#!/usr/bin/env python
# -*- coding:utf-8 -*-


from .api import Telegraph


class TeleNote(Telegraph):
    def __init__(self, access_token=None, reconnect_times=3, my_proxies=None,
                 timeout=5, author_name=None, short_name=None, author_url=None):
        super().__init__(access_token, reconnect_times, my_proxies, timeout)
        self.author_name = author_name
        self.short_name = short_name
        self.author_url = author_url

    def create_new_article(self, url_path, content=[{"tag":"p","children":["Hello, world!"]}], return_content=True):
        response = self.create_page(title=url_path, content=content, author_name=self.author_name,
                         author_url=self.author_url, return_content=return_content)
        return response["url"]

    def get_auth_url(self):
        fields = ["auth_url"]
        response = self.get_account_info(fields)
        return response["auth_url"]

    def create_my_account(self, replace_token=True):
        response = self.create_account(short_name=self.short_name, author_name=self.author_name,
                            author_url=self.author_url, replace_token=replace_token)
        return response
