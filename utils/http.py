import random

import requests

try:
    import simplejson as json
except ImportError:
    import json

import urllib3
import logging
import pendulum


from urllib.parse import urljoin, urlparse
from utils.settings import HEADERS_DEFAULT, PROXIES_LIST

log = logging.getLogger('HTTP')


def get_instance_for_request():
    """Added a method to increase the pool size for the connections."""
    sess = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=10000, pool_maxsize=10000)
    sess.mount('http://', adapter)
    sess.mount('https://', adapter)

    return sess


def check_status_code(response, status_code):

    if response:
        try:
            status_code = response.status_code
        except:
            pass
    return status_code


def store_http_information(url, error_info, status_code=None):
    pass
    # from contentstudio.models.elastic.monitor import HttpMonitor
    # domain_url = urlparse(url).netloc
    # http_item = HttpMonitor(url=url,
    #                         domain=domain_url,
    #                         error_info=error_info,
    #                         created_at=pendulum.now('UTC'))
    # if status_code:
    #     http_item.status_code = status_code
    # http_item.save()


def get_random_public_proxy():
    log.info('Loading random public proxy')

    # from contentstudio.models.mongo.model import Proxies
    # proxy_address = Proxies.random_proxy()
    # try:
    #     proxy = 'http://{0}'.format(proxy_address[0].ip_address)
    # except TypeError:
    #     proxy = 'http://{0}'.format(list(proxy_address)[0].ip_address)
    # return proxy


def retry_without_proxy(url, timeout, headers):
    response = None
    status_code = None
    try:
        response = requests.get(url, timeout=timeout, headers=headers)
    except requests.exceptions.SSLError:
        try:
            response = requests.get(url, timeout=timeout, headers=headers, verify=False)
        except Exception as ex:
            status_code = check_status_code(response, status_code)
            store_http_information(url, type(ex).__name__, status_code)
    except Exception as ex:
        status_code = check_status_code(response, status_code)
        store_http_information(url, type(ex).__name__, status_code)
    return response


class Requests():
    def __init__(self, fine_proxy=None, public_proxy=False):
        """
        :param fine_proxy: used for the social analyzer
        """
        self.set_proxy(public_proxy)
        self.text = None
        self.status_code = 0
        self.content = None
        self.url = None
        self.headers = {}
        self.fine_proxy = fine_proxy
        self.public_proxy = public_proxy

    def set_proxy(self, public_proxy):
        if public_proxy:
            proxy = get_random_public_proxy()
        else:
            pass
        #     MERGED_PROXIES = PROXIES_LIST
        #     proxy = random.choice(MERGED_PROXIES)
        # self.proxy = {
        #     "http": proxy,
        #     "https": proxy.replace('http://', 'https://')
        # }

    def get(self, url, use_proxy=False, headers=HEADERS_DEFAULT, timeout=60, backconnect=False):
        # url validation
        if not url.startswith('http://') and not url.startswith('https://'):
            if url.startswith('//'):
                url = 'http:' + url
            elif url.startswith('/'):
                url = 'http:/' + url
            else:
                url = 'http://' + url

        # changing the use_proxy to fine_proxy meanwhile we get the issue resolve from the d4networks.

        if use_proxy:
            if self.public_proxy:
                response = get_instance_for_request().get(url, timeout=timeout, proxies=self.proxy,
                                                          headers=headers)
            else:
                try:
                    response = get_instance_for_request().get(url, timeout=timeout, proxies=self.proxy,
                                                              headers=headers)
                except urllib3.exceptions.ProtocolError:
                    # In case of the bad status line error, we do not try to get with the proxy.
                    response = retry_without_proxy(url, timeout, headers)
                except requests.exceptions.SSLError:
                    # In case of the bad status line error, we do not try to get with the proxy.
                    response = retry_without_proxy(url, timeout, headers)
                except urllib3.exceptions.ReadTimeoutError:
                    response = retry_without_proxy(url, timeout, headers)
                except requests.exceptions.ProxyError:
                    response = retry_without_proxy(url, timeout, headers)
                except requests.exceptions.ConnectionError:
                    response = retry_without_proxy(url, timeout, headers)
                except requests.exceptions.ReadTimeout:
                    response = retry_without_proxy(url, timeout, headers)
                except requests.exceptions.TooManyRedirects:
                    response = retry_without_proxy(url, timeout, headers)

        else:
            response = None
            try:
                response = get_instance_for_request().get(url, timeout=timeout,
                                                          headers=headers)
            except requests.exceptions.SSLError:
                try:
                    response = requests.get(url, timeout=timeout, headers=headers, verify=False)
                except Exception as ex:
                    store_http_information(url, type(ex).__name__)
            except Exception as ex:
                store_http_information(url, type(ex).__name__)
        self.set_response(response)
        return response

    def post(self, url, body=None, use_proxy=False, headers=HEADERS_DEFAULT):
        if use_proxy:
            response = get_instance_for_request().post(url, data=body, proxies=self.proxy, headers=headers)
        else:
            response = get_instance_for_request().post(url, data=body, headers=headers)

        self.set_response(response)
        return self

    def set_response(self, response):
        if response:
            self.status_code = response.status_code
            self.content = response.content
            self.text = response.text
            self.url = response.url
            self.headers = response.headers


class SocialRequests(object):
    def __init__(self, access_token):
        self.access_token = access_token

    def send(self, path):
        request = Requests()
        path_join = path + '&access_token=%s' % self.access_token
        print(urljoin('https://graph.facebook.com/v2.8/', path_join))
        response = request.get(urljoin('https://graph.facebook.com/v2.8/', path_join))
        return json.loads(response.text)

    def fb_pageid_request(self, path):
        request = Requests()
        response = request.get(
            "https://graph.facebook.com/v2.7/" + path + "?fields=link,name,description,fan_count,category,username,picture&access_token=" + self.access_token + "&format=json")
        return json.loads(response.text)


class RequestConnection():
    def __init__(self):
        self._pool_size()

    def _pool_size(self):
        """Increase default pool size."""
        self.requests = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=1000, pool_maxsize=1000)
        self.requests.mount('http://', adapter)
        self.requests.mount('https://', adapter)

    def perform_request(self, url, **kwargs):
        """Performing request and returning a response"""
        url = self._url_join(url)
        if kwargs.get('proxy') and kwargs.get('proxy') == True:
            kwargs['proxies'] = self._random_proxy()
            kwargs.pop('proxy')  # remove proxy if present

        if kwargs.get('method') and kwargs.get('method') == 'POST':
            kwargs.pop('method')
            return self.requests.post(url, **kwargs)
        try:
            return self.requests.get(url, **kwargs)
        except requests.exceptions.SSLError:
            # In case of the bad status line error, we do not try to get with the proxy.
            return retry_without_proxy(url, 60, HEADERS_DEFAULT)
        except urllib3.exceptions.ReadTimeoutError:
            return retry_without_proxy(url, 60, HEADERS_DEFAULT)
        except requests.exceptions.ProxyError:
            return retry_without_proxy(url, 60, HEADERS_DEFAULT)
        except requests.exceptions.ConnectionError:
            return retry_without_proxy(url, 60, HEADERS_DEFAULT)
        except requests.exceptions.ReadTimeout:
            return retry_without_proxy(url, 60, HEADERS_DEFAULT)
        except requests.exceptions.TooManyRedirects:
            return retry_without_proxy(url, 60, HEADERS_DEFAULT)

    def _random_proxy(self):
        """Random proxy dict"""
        proxy = random.choice(PROXIES_LIST)
        return {
            "http": proxy,
            "https": proxy.replace('http://', 'https://')
        }

    def _url_join(self, url):
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'http://' + url
        return url
