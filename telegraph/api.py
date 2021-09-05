#!/usr/bin/env python
# -*- coding:utf-8 -*-


import json
import requests
from requests.exceptions import ConnectionError


class TelegraphException(Exception):
    pass


class TelegraphAPI(object):
    __slots__ = ('access_token', 'session', 'headers', 'reconnect_times', 'my_proxies', 'timeout')
    def __init__(self, access_token=None, reconnect_times=3, my_proxies=None, timeout=5):
        self.access_token = access_token
        self.timeout = timeout
        self.reconnect_times = reconnect_times
        self.my_proxies = my_proxies
        self.session = requests.session()
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

    def method(self, mehtod, values=None, path=""):
        values = values if values is not None else {}
        if "access_token" not in values and self.access_token:
            values['access_token'] = self.access_token
        req_url = "https://api.telegra.ph/{}/{}".format(mehtod, path)
        try:
            response = self.session.post(url=req_url, data=values, headers = self.headers,
                                         proxies=self.my_proxies, timeout=self.timeout).json()
            connected = True
        except ConnectionError:
            connected = False
        for reconnect_time in range(self.reconnect_times):
            if not connected:
                try:
                    response = self.session.post(url=req_url, data=values, headers = self.headers,
                                                 proxies=self.my_proxies, timeout=self.timeout).json()
                    connected = True
                except ConnectionError:
                    pass
            else:
                break
        if connected:
            try:
                return response["result"]
            except Exception:
                print(response)
        else:
            raise ConnectionError


class Telegraph(object):
    __slots__ = ("_telegraph")

    def __init__(self, access_token=None, reconnect_times=3, my_proxies=None, timeout=5):
        self._telegraph = TelegraphAPI(access_token, reconnect_times, my_proxies, timeout)

    def get_access_token(self):
        return self._telegraph.access_token

    def create_account(self,short_name, author_name=None,
                       author_url=None,replace_token=True):
        """

        :param short_name:
        :param author_name:
        :param author_url:
        :param replace_token:
        :return:dict
        """
        method = "createAccount"
        values = {
            'short_name': short_name,
            'author_name': author_name,
            'author_url': author_url
        }
        response = self._telegraph.method(method,values)
        if replace_token:
            self._telegraph.access_token = response.get("access_token")
        return response

    def edit_account_info(self, short_name=None, author_name=None, author_url=None):
        """

        :param short_name:
        :param author_name:
        :param author_url:
        :return:
        """
        method = "editAccountInfo"
        values = {
            'short_name': short_name,
            'author_name': author_name,
            'author_url': author_url
        }
        response = self._telegraph.method(method, values)
        return response

    def revoke_access_token(self):
        """

        :return:
        """
        method = "revokeAccessToken"
        values = None
        response = self._telegraph.method(method, values)
        self._telegraph.access_token = response.get('access_token')
        return response

    def get_page(self, path, return_content=True):
        """

        :param path:
        :param return_content:
        :param return_html:
        :return:
        """
        method = "getPage"
        values = {
            'return_content': return_content
        }
        response = self._telegraph.method(method, values, path)
        return response

    def create_page(self, title, content=None, author_name=None,
                    author_url=None, return_content=True):
        """

        :param title:
        :param content:
        :param html_content:
        :param author_name:
        :param author_url:
        :param return_content:
        :return:
        """
        content_json = json.dumps(content)
        method = "createPage"
        values = {
            'title': title,
            'author_name': author_name,
            'author_url': author_url,
            'content': content_json,
            'return_content': return_content
        }
        response = self._telegraph.method(method, values)
        return response

    def edit_page(self, path, title, content=None, author_name=None,
                  author_url=None, return_content=False):
        """

        :param path:
        :param title:
        :param content:
        :param author_name:
        :param author_url:
        :param return_content:
        :return:
        """
        content_json = json.dumps(content)
        method = "editPage"
        values = {
            'title': title,
            'author_name': author_name,
            'author_url': author_url,
            'content': content_json,
            'return_content': return_content
        }
        response = self._telegraph.method(method, values, path)
        return response

    def get_account_info(self, fields=None):
        """

        :param fields:
        :return:
        """
        method = "getAccountInfo"
        values = {
            'fields': json.dumps(fields) if fields else None
        }
        response = self._telegraph.method(method, values)
        return response

    def get_page_list(self, offset=0, limit=50):
        """

        :param offset:
        :param limit:
        :return:
        """
        method = "getPageList"
        values = {
            'offset': offset,
            'limit': limit
        }
        response = self._telegraph.method(method, values)
        return response

    def get_views(self, path, year=None, month=None, day=None, hour=None):
        """

        :param path:
        :param year:
        :param month:
        :param day:
        :param hour:
        :return:
        """
        method = "getViews"
        values = {
            'year': year,
            'month': month,
            'day': day,
            'hour': hour
        }
        response = self._telegraph.method(method, values)
        return response
