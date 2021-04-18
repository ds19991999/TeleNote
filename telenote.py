#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
-------------------------------------------------
   File Name：     run.py
   Description :
   Author :        admin
   date：          2019/12/4
-------------------------------------------------
   Change Activity:
                   2019/12/4
-------------------------------------------------
"""

import yaml, os
import random
import string
from telegraph.utils import TeleNote
from telegraph.color import Color


__author__ = 'admin'
clr = Color()


def read_config_file(config_path):
    with open(config_path, "r", encoding="utf-8") as config_file:
        config_data = yaml.safe_load(config_file.read())
    return config_data


def update_config_file(config_data, config_path):
    with open(config_path, "w", encoding="utf-8") as config_file:
        yaml.dump(config_data, config_file)


def generate_random_str(randomlength=5):
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str


def print_menu():
    clr.print_red_text("欢迎进入 telenote v0.1")
    clr.print_green_text("-" * 25)
    print("0" + "-" * 10 + "显示菜单")
    print("1" + "-" * 10 + "账户信息")
    print("2" + "-" * 10 + "文章列表")
    print("3" + "-" * 10 + "新建文章")
    print("q" + "-" * 10 + "退出系统")


def account_info(telenote:TeleNote):
    print("auth_url: {}".format(telenote.get_auth_url()))
    print("author_name: {}".format(telenote.author_name))
    print("short_name: {}".format(telenote.short_name))
    print("author_url: {}".format(telenote.author_url))
    print("access_token: {}".format(telenote._telegraph.access_token))


def my_articles(telenote:TeleNote, offset=0, limit=50):
    response = telenote.get_page_list(offset, limit)
    total_count = response["total_count"]
    clr.print_green_text("文章总数：{}".format(total_count))
    clr.print_green_text("认证地址：{}".format(telenote.get_auth_url()))
    clr.print_green_text("序号".ljust(5)+"文章标题".ljust(10)+"浏览量".ljust(10)+"文章链接".ljust(20) + "\n")
    pages = response["pages"]
    page_num = 0
    for page in pages:
        page_num += 1
        url = page["url"].ljust(20)
        title = page["title"].ljust(10)
        views = str(page["views"]).ljust(10)
        article = "{}: {} {} {}".format(str(page_num).ljust(5), title, views, url)
        print(article)


def Entrance(config_path):
    config_data = read_config_file(config_path)
    access_token = config_data["telegraph"]["access_token"]
    author_name = config_data["telegraph"]["author_name"]
    author_url = config_data["telegraph"]["author_url"]
    short_name = config_data["telegraph"]["short_name"]
    proxy = config_data["proxy"]
    telenote = TeleNote(access_token=access_token, my_proxies=proxy, author_name=author_name,
                        short_name=short_name,author_url=author_url)
    if access_token == None:
        response = telenote.create_my_account()
        access_token = config_data["telegraph"]["access_token"] = response["access_token"]
        update_config_file(config_data, config_path)
    # 更新账户信息
    telenote.edit_account_info(short_name=short_name, author_url=author_url, author_name=author_name)
    clr.print_green_text("当前账户信息:")
    account_info(telenote)
    os.system("pause")
    os.system("cls")
    print_menu()
    while True:
        command = input("请输入操作符：").strip()
        if command == "0":
            os.system("cls")
            print_menu()
        elif command == "1":
            account_info(telenote)
            os.system("pause")
            os.system("cls")
            print_menu()
        elif command == "2":
            my_articles(telenote, offset=0, limit=10000)
            os.system("pause")
            os.system("cls")
            print_menu()
        elif command == "3":
            url_path = generate_random_str()
            new_url = telenote.create_new_article(url_path)
            auth_url = telenote.get_auth_url()
            clr.print_green_text("文章链接：{}".format(new_url))
            clr.print_green_text("认证地址：{}".format(auth_url))
        elif command == "q" or command == "Q":
            os.system("cls")
            os.system(exit())
        else:
            os.system("cls")
            print_menu()
            clr.print_red_text("[----] 输入指令序号错误！")


if __name__ == "__main__":
    Entrance("config.yaml")

