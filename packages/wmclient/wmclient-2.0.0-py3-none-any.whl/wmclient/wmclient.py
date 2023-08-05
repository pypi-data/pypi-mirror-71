import json
import os
import threading
from functools import lru_cache
from io import BytesIO

import logging
import pycurl

__version__ = "2.0.1"
__client_version__ = "wurfl-microservice-python_%s" % __version__
__default_http_timeout__ = 10000
config_path = ""


def read_cache_size():
    default_cache_size = 200000
    if "WM_CACHE_SIZE" in os.environ:
        return int(os.environ["WM_CACHE_SIZE"])
    return default_cache_size


cache_size = read_cache_size()

logger = logging.getLogger("wurfl-microservice")


class JsonDeviceOsVersion:

    def __init__(self, info_dict):
        self.device_os = info_dict["device_os"]
        self.device_os_version = info_dict["device_os_version"]


class JSONModelMktName:

    def __init__(self, info_dict):
        self.brand_name = info_dict["brand_name"]
        self.model_name = info_dict["model_name"]


class WmClient:

    def __init__(self):
        self.scheme = "http"
        self.host = ""
        self.port = 80
        self.base_uri = ""
        self.device_makes = []
        self.requested_static_caps = []
        self.requested_virtual_caps = []
        self.important_headers = []
        self.device_os_lock = threading.Lock()
        self.device_makes_lock = threading.Lock()
        self.device_OSes = []
        self.curl_post = pycurl.Curl()
        self.curl_post.setopt(pycurl.TIMEOUT_MS, __default_http_timeout__)
        self.curl_post.setopt(pycurl.HTTPHEADER, ['Accept: application/json',
                                                  'Content-Type: application/json'])
        self.curl_get = pycurl.Curl()
        self.curl_get.setopt(pycurl.TIMEOUT_MS, __default_http_timeout__)
        self.curl_get.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])

    @staticmethod
    def create(scheme, host, port, baseURI):
        """Creates a new WURFL Microservice client. The client has a default timeout of 10 seconds (set as 10000
        milliseconds). If not scheme is give, client assumes a 'http' value."""
        client = WmClient()
        if len(scheme) > 0:
            client.scheme = scheme
        client.host = host
        client.port = port
        client.base_uri = baseURI

        info = client.get_info()
        client.important_headers = info.important_headers
        client.staticCaps = sorted(info.static_capabilities)
        client.virtualCaps = sorted(info.virtual_capabilities)

        return client

    def set_http_timeout(self, timeout):
        """Sets HTTP connection timeout in milliseconds"""
        if timeout is None or timeout <= 0:
            self.curl_post.setopt(pycurl.TIMEOUT_MS, __default_http_timeout__)
        else:
            self.curl_post.setopt(pycurl.TIMEOUT_MS, timeout)

        if timeout is None or timeout <= 0:
            self.curl_get.setopt(pycurl.TIMEOUT_MS, __default_http_timeout__)
        else:
            self.curl_get.setopt(pycurl.TIMEOUT_MS, timeout)

    def destroy(self):
        """Closes and deallocates all resources used to connect to server.
        Function calls made after this one will cause error"""
        self.curl_get.close()
        self.curl_get = None

        self.curl_post.close()
        self.curl_post = None

    def get_info(self):
        """Returns info about WURFL microservice server.
        It raises a WmClientError in case of connection errors/timeouts"""

        msg = "Client creation failed. Unable to connect to WURFL microservice server - "
        data = BytesIO()
        try:
            # performs a GET using pycurl
            self.curl_get.setopt(self.curl_get.URL, self.__create_URL("/v2/getinfo/json"))
            self.curl_get.setopt(self.curl_get.WRITEFUNCTION, data.write)
            self.curl_get.perform()
            res_code = self.curl_get.getinfo(pycurl.HTTP_CODE)

        except ConnectionError as e:
            if hasattr(e, 'message'):
                msg += e.message
                raise WmClientError(msg)
        except Exception:
            raise WmClientError(msg)

        if 200 <= res_code < 400:
            info = json.loads(data.getvalue().decode(encoding='UTF-8'))
            data.close()
            return JsonInfoData(info)
        else:
            msg = "get_info - Unable to get WURFL microservice server info - response code: " + str(res_code)
            logging.error(msg)
            raise WmClientError(msg)

    def __create_URL(self, path):
        url = self.scheme + "://" + self.host
        if self.port > 0:
            url += ":" + str(self.port)
        if len(self.base_uri) > 0:
            return url + "/" + self.base_uri + path
        else:
            return url + path

    def has_static_capability(self, capName):
        """returns True if the given static capability is handled by this client, False otherwise"""
        return capName in self.staticCaps

    def has_virtual_capability(self, capName):
        """returns True if the given virtual capability is handled by this client, False otherwise"""
        return capName in self.virtualCaps

    def set_requested_static_capabilities(self, capsList):
        """sets the list of static capabilities handled by this client"""
        if capsList is None:
            self.requested_static_caps = None
            self.clear_cache()
            return

        stCaps = []
        for name in capsList:
            if self.has_static_capability(name):
                stCaps.append(name)

        self.requested_static_caps = stCaps
        self.clear_cache()

    def set_requested_virtual_capabilities(self, capsList):
        """sets the list of virtual capabilities handled by this client"""
        if capsList is None:
            self.requested_virtual_caps = None
            self.clear_cache()
            return

        vCaps = []
        for name in capsList:
            if self.has_virtual_capability(name):
                vCaps.append(name)

        self.requested_virtual_caps = vCaps
        self.clear_cache()

    def set_requested_capabilities(self, capsList):
        """sets the list of virtual and static capabilities handled by this client"""
        if capsList is None:
            self.requested_static_caps = None
            self.requested_virtual_caps = None
            self.__internal_request.cache_clear()
            return

        capNames = []
        vcapNames = []

        for name in capsList:
            if self.has_static_capability(name):
                capNames.append(name)
            else:
                if self.has_virtual_capability(name):
                    vcapNames.append(name)

        if len(capNames) > 0:
            self.requested_static_caps = capNames

        if len(vcapNames) > 0:
            self.requested_virtual_caps = vcapNames
        self.__internal_request.cache_clear()

    @lru_cache(maxsize=cache_size)
    def __internal_request(self, path, req):

        device = None
        # Buffer where data sent from the server are written
        data = BytesIO()
        url = self.__create_URL(path)
        try:

            self.curl_post.setopt(self.curl_post.URL, url)
            # prepares request payload
            d = json.dumps(req.__dict__)
            payload = d.encode()
            # Sets request method to POST,
            # and data to send in request body.
            self.curl_post.setopt(self.curl_post.POSTFIELDS, payload)
            self.curl_post.setopt(self.curl_post.WRITEFUNCTION, data.write)
            self.curl_post.perform()
            res_code = self.curl_post.getinfo(pycurl.HTTP_CODE)
            if 200 <= res_code < 400:
                json_response = json.loads(data.getvalue().decode(encoding='UTF-8'))
                device = JsonDeviceData(json_response)
                data.close()
                if device.error != "":
                    raise WmClientError("Unable to complete request to WM server: " + device.error)

        except Exception as e:
            logging.error(str(e))
            if isinstance(e, WmClientError):
                raise e
            else:
                msg = self.__format_except_message__(e, "Unable to complete request to WM server: ")
                logging.error(msg)
                raise WmClientError(msg)
        finally:
            # closing buffer
            data.close()
        return device

    def lookup_useragent(self, useragent):
        """performs a device detection from the given User-Agent. If the User-Agent is None or empty a generic device
        is returned """
        headers = {"User-Agent": useragent}
        request = Request(lookup_headers=headers, requestedCaps=self.requested_static_caps,
                          requestedVcaps=self.requested_virtual_caps, wurflId=None, cache_type=HEADERS_CACHE_TYPE,
                          important_headers=self.important_headers)
        return self.__internal_request("/v2/lookupuseragent/json", request)

    def lookup_request(self, req):

        """performs a device detection from the headers carried by the give HTTP request.
        The request object is assumed to be the one used in requests python framework.
        If the User-Agent header is None or empty a generic device
                is returned """
        if req is None:
            raise WmClientError("requests.Request cannot be None")

        reqHeaders = dict()
        for hname in self.important_headers:
            if hname in req.headers:
                hval = req.headers[hname]
                if len(hval) > 0:
                    reqHeaders[hname] = hval

        request = Request(lookup_headers=reqHeaders, requestedCaps=self.requested_static_caps,
                          requestedVcaps=self.requested_virtual_caps, wurflId=None,
                          important_headers=self.important_headers, cache_type=HEADERS_CACHE_TYPE)
        return self.__internal_request("/v2/lookuprequest/json", request)

    def lookup_device_id(self, wurflId):
        """Retrieves a device with the given WURFL ID. If the WURFL ID is None, empty or wring a WMClientError is
        raised """

        request = Request(lookup_headers=None, requestedCaps=self.requested_static_caps,
                          requestedVcaps=self.requested_virtual_caps, wurflId=wurflId,
                          important_headers=self.important_headers, cache_type=DEVICE_ID_CACHE_TYPE)
        return self.__internal_request("/v2/lookupdeviceid/json", request)

    def get_all_OSes(self):
        """:return a list of all device OS"""
        self.__load_device_OSes_data()
        return self.device_OSes

    def __load_device_OSes_data(self):
        self.device_os_lock.acquire()
        devOsNotEmpty = (self.device_OSes is not None) & (len(self.device_OSes) > 0)
        if devOsNotEmpty:
            if self.device_os_lock.locked():
                self.device_os_lock.release()
            return
        data = BytesIO()
        try:
            url = self.__create_URL("/v2/alldeviceosversions/json")
            self.curl_get.setopt(self.curl_get.URL, url)
            self.curl_get.setopt(self.curl_get.WRITEFUNCTION, data.write)
            self.curl_get.perform()
            res_code = self.curl_get.getinfo(pycurl.HTTP_CODE)
            if not (200 <= res_code < 400):
                raise WmClientError("Unable to get device OSes data - response code: " + str(res_code))
            else:
                strOSes = json.loads(data.getvalue().decode(encoding='UTF-8'))
                data.close()
            devOses = []
            ddict = dict()
            for osVer in strOSes:

                devOsVer = JsonDeviceOsVersion(osVer)
                if devOsVer.device_os not in devOses:
                    devOses.append(devOsVer.device_os)

                if devOsVer.device_os not in ddict:
                    ddict[devOsVer.device_os] = []
                ddict[devOsVer.device_os].append(devOsVer.device_os_version)

            if not self.device_os_lock.locked():
                self.device_os_lock.acquire()
            self.device_OSes = devOses
            self.deviceOsVersionsMap = ddict
            self.device_os_lock.release()
        except Exception as e:
            msg = self.__format_except_message__(e, "An error occurred getting device os name and version data - {}"
                                        .format(str(e)))
            logging.error(msg)
            data.close()
            raise WmClientError(msg)
        finally:
            if self.device_os_lock.locked():
                self.device_os_lock.release()

    def get_all_versions_for_OS(self, osName):
        """:return a list of all the known versions for the given device OS"""
        self.__load_device_OSes_data()
        if osName in self.deviceOsVersionsMap:
            osVers = self.deviceOsVersionsMap[osName]
            for ver in osVers:
                if "" == ver:
                    osVers.remove(ver)
            return osVers
        else:
            msg = "Error getting data from WM server: {} does not exist".format(osName)
            raise WmClientError(msg)

    def __load_device_makes_data(self):

        # If deviceMakes cache has values everything has already been loaded, thus we exit
        self.device_makes_lock.acquire()
        if len(self.device_makes) > 0:
            if self.device_makes_lock.locked():
                self.device_makes_lock.release()
                return

        # No values already loaded, let's do it.
        data = BytesIO()
        try:
            url = self.__create_URL("/v2/alldevices/json")
            self.curl_get.setopt(self.curl_get.URL, url)
            self.curl_get.setopt(self.curl_get.WRITEFUNCTION, data.write)
            self.curl_get.perform()
            res_code = self.curl_get.getinfo(pycurl.HTTP_CODE)
            if not (200 <= res_code < 400):
                raise WmClientError("Unable to get device makers data - response code: " + str(res_code))
            else:
                localMakeModels = json.loads(data.getvalue().decode(encoding='UTF-8'))
                data.close()

                dmMap = dict()
                devMakes = []
                for jmkModel in localMakeModels:
                    mkModel = JSONModelMktName(jmkModel)
                    if mkModel.brand_name not in dmMap:
                        devMakes.append(mkModel.brand_name)

                    mdMkNames = dmMap.get(mkModel.brand_name)
                    if mdMkNames is None:
                        mdMkNames = []
                        dmMap[mkModel.brand_name] = mdMkNames

                    mdMkNames.append(mkModel)
                    if not self.device_makes_lock.locked():
                        self.device_makes_lock.acquire()
                    self.deviceMakesMap = dmMap
                    self.device_makes = devMakes
                    if self.device_makes_lock.locked():
                        self.device_makes_lock.release()
        except Exception as e:
            msg = self.__format_except_message__(e, "An error occurred getting makes and model data ")
            logging.error(msg)
            raise WmClientError(msg)

    def get_all_device_makes(self):
        """:return a list of all device makers"""
        self.__load_device_makes_data()
        return self.device_makes

    def get_all_devices_for_make(self, make):
        """:return a list of all device models for the given maker"""
        self.__load_device_makes_data()

        if make in self.deviceMakesMap:
            mdMks = self.deviceMakesMap[make]
            return mdMks
        else:
            msg = "Error getting data from WM server: {} does not exist".format(make)
            raise WmClientError(msg)

    def cache_info(self):
        """:return the current state of WMClient internal cache (hits, misses, max size)"""
        return self.__internal_request.cache_info()

    def clear_cache(self):
        """clears WM client internal cache"""
        return self.__internal_request.cache_clear()

    def get_api_version(self):
        """:return the version of this WM Client"""
        return __client_version__

    def __format_except_message__(self, e, msg):
        if hasattr(e, 'message'):
            fmsg = msg + e.message
            return fmsg
        else:
            return msg


class WmClientError(Exception):
    def __init__(self, message):
        self.message = message

HEADERS_CACHE_TYPE = "head-cache"
DEVICE_ID_CACHE_TYPE = "dId-cache"


class JsonInfoData:

    def __init__(self, info_dict):
        self.wurfl_api_version = info_dict["wurfl_api_version"]
        self.wurfl_info = info_dict["wurfl_info"]
        self.wm_version = info_dict["wm_version"]
        self.important_headers = info_dict["important_headers"]
        self.static_capabilities = info_dict["static_caps"]
        self.virtual_capabilities = info_dict["virtual_caps"]


class JsonDeviceData:

    def __init__(self, info_dict):
        self.error = info_dict["error"]
        self.api_version = info_dict["apiVersion"]
        self.capabilities = info_dict["capabilities"]
        self.mtime = int(info_dict["mtime"])
        self.ltime = info_dict["ltime"]


class Request:
    def __init__(self, lookup_headers, requestedCaps, requestedVcaps, wurflId, cache_type, important_headers):
        self.lookup_headers = lookup_headers
        self.requested_caps = requestedCaps
        self.requested_vcaps = requestedVcaps
        self.wurfl_id = wurflId
        self.cache_type = cache_type
        self.important_headers = important_headers
        self.key = None

    def __eq__(self, other):
        if self is None or other is None:
            return False
        if self.cache_type == DEVICE_ID_CACHE_TYPE:
            return self.wurfl_id == other.wurfl_id
        else:
            return self.get_user_agent_cache_key() == other.get_user_agent_cache_key()

    def __hash__(self):
        return hash(self.get_user_agent_cache_key())

    def get_user_agent_cache_key(self):

        if self.key is not None:
            return self.key

        key = ""
        if (self.lookup_headers is None or len(self.lookup_headers) == 0) \
                & (HEADERS_CACHE_TYPE == self.cache_type):
            self.key = ""
            return key

        # if cache type is device id we use wurfl_id as cache key
        if DEVICE_ID_CACHE_TYPE == self.cache_type:
            self.key = self.wurfl_id
            return self.key

        # Using important headers array preserves header name order
        for h in self.important_headers:
            if h in self.lookup_headers:
                hval = self.lookup_headers[h]
                if hval is not None:
                    key += hval
        self.key = key
        return self.key
