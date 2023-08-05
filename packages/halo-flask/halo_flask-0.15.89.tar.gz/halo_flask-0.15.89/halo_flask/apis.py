from __future__ import print_function

# python
import datetime
import importlib
import logging
import time
from abc import ABCMeta

import requests

from .classes import AbsBaseClass
from .exceptions import MaxTryHttpException, ApiError,NoApiDefinitionError
from .logs import log_json
from .reflect import Reflect
from .settingsx import settingsx
from halo_flask.const import LOC,DEV,TST,PRD
from .flask.utilx import Util
from .const import HTTPChoice,SYSTEMChoice,LOGChoice

settings = settingsx()

# DRF



logger = logging.getLogger(__name__)



from halo_flask.circuitbreaker import CircuitBreaker
class MyCircuitBreaker(CircuitBreaker):
    def __init__(self):
        print("init MyCircuitBreaker")
        FAILURE_THRESHOLD =  self.get_failure_threshold()
        RECOVERY_TIMEOUT = self.get_recovery_timeout()
        EXPECTED_EXCEPTION = Exception
        super(MyCircuitBreaker, self).__init__(FAILURE_THRESHOLD,RECOVERY_TIMEOUT,EXPECTED_EXCEPTION)

    def get_failure_threshold(self):
        FAILURE_THRESHOLD = 3
        if settings.HTTP_MAX_RETRY:
            FAILURE_THRESHOLD = settings.HTTP_MAX_RETRY
        return FAILURE_THRESHOLD

    def get_recovery_timeout(self):
        RECOVERY_TIMEOUT = 15
        if settings.HTTP_RETRY_SLEEP:
            RECOVERY_TIMEOUT = settings.HTTP_RETRY_SLEEP
        return RECOVERY_TIMEOUT


class AbsBaseApi(AbsBaseClass):
    __metaclass__ = ABCMeta

    name = None
    op = HTTPChoice.get.value
    url = None
    api_type = None
    halo_context = None
    cb = MyCircuitBreaker()

    def __init__(self, halo_context, method=None):
        self.halo_context = halo_context
        if method:
            self.op = method
        self.url, self.api_type = self.get_url_str()
        if settings.CIRCUIT_BREAKER:
            self.cb._name = self.name

    @cb
    def do_cb_request(self,method, url, timeout, data=None, headers=None, auth=None):
        print("do MyCircuitBreaker")
        return requests.request(method, url, data=data, headers=headers,
                         timeout=timeout, auth=auth)

    def do_request(self, method, url, timeout, data=None, headers=None, auth=None):
        if settings.CIRCUIT_BREAKER:
            return self.do_cb_request(method, url, timeout, data, headers, auth)
        return requests.request(method, url, data=data, headers=headers,
                                timeout=timeout, auth=auth)

    def exec_client(self, halo_context, method, url, api_type, timeout, data=None, headers=None, auth=None):
        """

        :param halo_context:
        :param method:
        :param url:
        :param api_type:
        :param timeout:
        :param data:
        :param headers:
        :return:
        """

        msg = "Max Try for url: ("+str(settings.HTTP_MAX_RETRY)+") " + str(url)
        for i in range(0, settings.HTTP_MAX_RETRY):
            logger.debug("try index: " + str(i), extra=log_json(halo_context))
            try:
                logger.debug("try: " + str(i), extra=log_json(halo_context))
                ret = self.do_request(method, url, timeout, data=data, headers=headers, auth=auth)
                logger.debug("request status_code=" + str(ret.status_code) +" content=" + str(ret.content), extra=log_json(halo_context))
                if ret.status_code >= 500:
                    continue
                if 200 > ret.status_code or 500 > ret.status_code >= 300:
                    err = ApiError("error status_code " + str(ret.status_code) + " in : " + url)
                    err.status_code = ret.status_code
                    err.stack = None
                    raise err
                return ret
            except requests.exceptions.ReadTimeout as e:  # this confirms you that the request has reached server
                logger.debug(str(e))
                logger.debug(
                    "ReadTimeout " + str(
                        settings.SERVICE_READ_TIMEOUT_IN_MS) + " in method=" + method + " for url=" + url,
                    extra=log_json(halo_context))
                continue
            except requests.exceptions.ConnectTimeout as e:
                logger.debug(str(e))
                logger.debug("ConnectTimeout in method=" + str(
                    settings.SERVICE_CONNECT_TIMEOUT_IN_MS) + " in method=" + method + " for url=" + url,
                             extra=log_json(halo_context))
                continue
        raise MaxTryHttpException(msg)

    def get_url_str(self):
        """

        :return:
        """
        api_config = settings.API_CONFIG
        logger.debug("api_config: " + str(api_config), extra=log_json(self.halo_context))
        if api_config and self.name in api_config:
            return api_config[self.name]["url"], api_config[self.name]["type"]
        raise NoApiDefinitionError(self.name)

    def set_api_url(self, key, val):
        """

        :param key:
        :param val:
        :return:
        """
        strx = self.url
        strx = strx.replace("$" + str(key), str(val))
        logger.debug("url replace var: " + strx, extra=log_json(self.halo_context))
        self.url = strx
        return self.url

    def set_api_base(self, base_url):
        """

        :param query:
        :return:
        """
        strx = self.url
        if "base_url" in self.url:
            strx = strx.replace("base_url",base_url)
        logger.debug("url add base: " + strx, extra=log_json(self.halo_context))
        self.url = strx
        return self.url

    def set_api_query(self, query):
        """

        :param query:
        :return:
        """
        strx = self.url
        if "?" in self.url:
            strx = strx + "&" + query
        else:
            strx = strx + "?" + query
        logger.debug("url add query: " + strx, extra=log_json(self.halo_context))
        self.url = strx
        return self.url

    def set_api_params(self, params):
        """

        :param params:
        :return:
        """
        if not params or len(params) == 0:
            return self.url
        strx = self.url
        for key in params:
            val = params[key]
            query = key+"="+val
            if "?" in self.url:
                strx = strx + "&" + query
            else:
                strx = strx + "?" + query
        logger.debug("url add query: " + strx, extra=log_json(self.halo_context))
        self.url = strx
        return self.url

    def process(self, method, url, timeout, data=None, headers=None,auth=None):
        """

        :param method:
        :param url:
        :param timeout:
        :param data:
        :param headers:
        :return:
        """
        try:
            logger.debug("Api name: " + self.name +" method: " + str(method) + " url: " + str(url) + " headers:" + str(headers), extra=log_json(self.halo_context))
            now = datetime.datetime.now()
            ret = self.exec_client(self.halo_context, method, url, self.api_type, timeout, data=data, headers=headers, auth=auth)
            total = datetime.datetime.now() - now
            logger.info(LOGChoice.performance_data.value, extra=log_json(self.halo_context,
                                                                         {LOGChoice.type.value: SYSTEMChoice.api.value, LOGChoice.milliseconds.value: int(total.total_seconds() * 1000),
                                                       LOGChoice.url.value: str(url)}))
            logger.debug("ret: " + str(ret), extra=log_json(self.halo_context))
            return ret
        except requests.ConnectionError as e:
            msg = str(e)
            logger.debug("error: " + msg, extra=log_json(self.halo_context))
            er = ApiError(msg,e)
            er.status_code = 500
            raise er
        except requests.HTTPError as e:
            msg = str(e)
            logger.debug("error: " + msg, extra=log_json(self.halo_context))
            er = ApiError(msg,e)
            er.status_code = 500
            raise er
        except requests.Timeout as e:
            msg = str(e)
            logger.debug("error: " + msg, extra=log_json(self.halo_context))
            er = ApiError(msg,e)
            er.status_code = 500
            raise er
        except requests.RequestException as e:
            msg = str(e)
            logger.debug("error: " + msg, extra=log_json(self.halo_context))
            er = ApiError(msg,e)
            er.status_code = 500
            raise er
        except ApiError as e:
            msg = str(e)
            logger.debug("error: " + msg, extra=log_json(self.halo_context))
            raise e

    def run(self,timeout, headers=None, auth=None,data=None):
        if headers is None:
            headers = headers
        return self.process(self.op, self.url, timeout, headers=headers,auth=auth,data=data)

    def get(self, timeout, headers=None,auth=None):
        """

        :param timeout:
        :param headers:
        :return:
        """
        if headers is None:
            headers = headers
        return self.process(HTTPChoice.get.value, self.url, timeout, headers=headers,auth=auth)

    def post(self, data, timeout, headers=None,auth=None):
        """

        :param data:
        :param timeout:
        :param headers:
        :return:
        """
        logger.debug("payload=" + str(data))
        if headers is None:
            headers = headers
        return self.process(HTTPChoice.post.value, self.url, timeout, data=data, headers=headers,auth=auth)

    def put(self, data, timeout, headers=None,auth=None):
        """

        :param data:
        :param timeout:
        :param headers:
        :return:
        """
        if headers is None:
            headers = headers
        return self.process(HTTPChoice.put.__str__(), self.url, timeout, data=data, headers=headers,auth=auth)

    def patch(self, data, timeout, headers=None,auth=None):
        """

        :param data:
        :param timeout:
        :param headers:
        :return:
        """
        if headers is None:
            headers = headers
        return self.process(HTTPChoice.patch.value, self.url, timeout, data=data, headers=headers,auth=auth)

    def delete(self, timeout, headers=None,auth=None):
        """

        :param timeout:
        :param headers:
        :return:
        """
        if headers is None:
            headers = headers
        return self.process(HTTPChoice.delete.value, self.url, timeout, headers=headers,auth=auth)

    def fwd_process(self, typer, request, vars, headers,auth=None):
        """

        :param typer:
        :param request:
        :param vars:
        :param headers:
        :return:
        """
        verb = typer.value
        if verb == HTTPChoice.get.value or HTTPChoice.delete.value:
            data = None
        else:
            data = request.data
        return self.process(verb, self.url, Util.get_timeout(request), data=data, headers=headers,auth=auth)

class ApiMngr(AbsBaseClass):
    API_LIST = []


    def __init__(self, halo_context):
        logger.debug("ApiMngr=" + str(halo_context))
        self.halo_context = halo_context

    @staticmethod
    def set_api_list(list):
        """

        :param name:
        :return:
        """
        logger.debug("set_api_list")
        if list:
            ApiMngr.API_LIST = list

    @staticmethod
    def get_api(name):
        """

        :param name:
        :return:
        """
        logger.debug("get_api=" + name)
        if name in ApiMngr.API_LIST:
            return ApiMngr.API_LIST[name]
        return None

    def get_api_instance(self, class_name, *args):
        return Reflect.do_instantiate(__name__,class_name,AbsBaseApi,self.halo_context)


SSM_CONFIG = None
SSM_APP_CONFIG = None
def load_api_config(stage_type,ssm_type,func_name,API_CONFIG):
    global SSM_CONFIG
    global SSM_APP_CONFIG

    #if stage_type == LOC:
    # from halo_flask.ssm import get_config as get_config
    try:
        from halo_flask.halo_flask.ssm import get_config
    except:
        from halo_flask.ssm import get_config

    SSM_CONFIG = get_config(ssm_type)
    # set_param_config(AWS_REGION, 'DEBUG_LOG', '{"val":"false"}')
    # SSM_CONFIG.get_param("test")

    # from halo_flask.ssm import get_config as get_config
    try:
        from halo_flask.halo_flask.ssm import get_app_config
    except:
        from halo_flask.ssm import get_app_config

    SSM_APP_CONFIG = get_app_config(ssm_type)

    # api_config:{'About': {'url': 'http://127.0.0.1:7000/about/', 'type': 'api'}, 'Task': {'url': 'http://127.0.0.1:7000/task/$upcid/', 'type': 'api'}, 'Curr': {'url': 'http://127.0.0.1:7000/curr/', 'type': 'api'}, 'Top': {'url': 'http://127.0.0.1:7000/top/', 'type': 'api'}, 'Rupc': {'url': 'http://127.0.0.1:7000/upc/$upcid/', 'type': 'api'}, 'Upc': {'url': 'http://127.0.0.1:7000/upc/$upcid/', 'type': 'api'}, 'Contact': {'url': 'http://127.0.0.1:7000/contact/', 'type': 'api'}, 'Fail': {'url': 'http://127.0.0.1:7000/fail/', 'type': 'api'}, 'Rtask': {'url': 'http://127.0.0.1:7000/task/$upcid/', 'type': 'api'}, 'Page': {'url': 'http://127.0.0.1:7000/page/$upcid/', 'type': 'api'}, 'Sim': {'url': 'http://127.0.0.1:7000/sim/', 'type': 'api'}, 'Google': {'url': 'http://www.google.com', 'type': 'service'}}
    for item in SSM_APP_CONFIG.cache.items:
        if item not in [func_name, 'DEFAULT']:
            url = SSM_APP_CONFIG.get_param(item)["url"]
            logger.debug(item + ":" + url)
            for key in API_CONFIG:
                current = API_CONFIG[key]
                new_url = current["url"]
                if "service://" + item in new_url:
                    API_CONFIG[key]["url"] = new_url.replace("service://" + item, url)
    logger.debug(str(API_CONFIG))





##################################### test #########################

class CnnApi(AbsBaseApi):
    name = 'Cnn'

class GoogleApi(AbsBaseApi):
    name = 'Google'

class TstApi(AbsBaseApi):
    name = 'Tst'

API_LIST = {"Google": 'GoogleApi', "Cnn": "CnnApi","Tst":"TstApi"}

ApiMngr.set_api_list(API_LIST)
