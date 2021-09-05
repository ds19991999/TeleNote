#!/usr/bin/env python
# -*- coding:utf-8 -*-


from rich import print
from rich.table import Column, Table
import os
import yaml
import random
import string
from telegraph import TeleNote


CLEAR = "cls" if os.name == "nt" else "clear"
MENUE_HELP = """
[bold yellow]🎉🎉🎉欢迎进入 [bold green]telegraph[/bold green] 命令行 [bold green]v0.01[/bold green][/bold yellow]

[bold green]help)[/bold green] 查看帮助 | h
[bold green]exit)[/bold green] 退出系统 | q | Ctrl+C
[bold green]me)[/bold green] 账户信息 | m
[bold green]list)[/bold green] 文章列表 | l | ls | ll
[bold green]new)[/bold green] 新建文章 | n

----------------------------------------------------------------
"""


def read_config_file(config_path):
    with open(config_path, "r", encoding="utf-8") as config_file:
        config_data = yaml.safe_load(config_file.read())
    return config_data


def update_config_file(config_data, config_path):
    with open(config_path, "w", encoding="utf-8") as config_file:
        yaml.dump(config_data, config_file)


def generate_random_str(head, randomlength=5):
    str_list = [random.choice(string.digits + string.ascii_letters)
                for i in range(randomlength)]
    random_str = ''.join(str_list)
    return head + "-" + random_str.lower()


def print_menu():
    print(MENUE_HELP)


def print_account_info(telenote: TeleNote):
    print("[bold yellow]auth_url:[/bold yellow] {}".format(telenote.get_auth_url()))
    print("[bold yellow]author_name:[/bold yellow] {}".format(telenote.author_name))
    print("[bold yellow]short_name:[/bold yellow] {}".format(telenote.short_name))
    print("[bold yellow]author_url:[/bold yellow] {}".format(telenote.author_url))
    print("[bold yellow]access_token:[/bold yellow] {}".format(telenote._telegraph.access_token))


def my_articles(telenote: TeleNote, offset=0, limit=50):
    response = telenote.get_page_list(offset, limit)
    total_count = response["total_count"]
    print("[bold green]文章总数：[/bold green]{}".format(total_count))
    print("[bold green]认证地址：[/bold green]{}".format(telenote.get_auth_url()))
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("序号", width=12)
    table.add_column("文章标题")
    table.add_column("浏览量")
    table.add_column("文章链接")
    pages = response["pages"]
    page_num = 0
    for page in pages:
        page_num += 1
        url = page["url"].ljust(20)
        title = page["title"].ljust(10)
        views = str(page["views"]).ljust(10)
        table.add_row(str(page_num), title, str(views), url)
    print(table)


def main(config_path):
    config_data = read_config_file(config_path)
    access_token = config_data["telegraph"]["access_token"]
    author_name = config_data["telegraph"]["author_name"]
    author_url = config_data["telegraph"]["author_url"]
    short_name = config_data["telegraph"]["short_name"]
    proxy = config_data["proxy"]
    telenote = TeleNote(access_token=access_token, my_proxies=proxy, author_name=author_name,
                        short_name=short_name, author_url=author_url)
    if access_token == None:
        response = telenote.create_my_account()
        access_token = config_data["telegraph"]["access_token"] = response["access_token"]
        update_config_file(config_data, config_path)
    # 更新账户信息
    telenote.edit_account_info(
        short_name=short_name, author_url=author_url, author_name=author_name)
    print_menu()
    while True:
        try:
            print("[bold cyan]>>> [/bold cyan]", end="")
            command = input().lower().strip()
            if command  == "help" or command == "h":
                os.system(CLEAR)
                print_menu()
            elif command  == "me" or command == "m":
                print_account_info(telenote)
            elif command in ["list", "ls", "ll", "l"]:
                my_articles(telenote, offset=0, limit=10000)
            elif command  == "new" or command == "n":
                url_path = generate_random_str(head=author_name)
                new_url = telenote.create_new_article(url_path)
                auth_url = telenote.get_auth_url()
                print("文章链接：{}".format(new_url))
                print("认证地址：{}".format(auth_url))
            elif command == "q" or command == "exit":
                os.system(exit())
            elif command == "cls" or command == "clear":
                os.system(CLEAR)
                print_menu()
            else:
                os.system(command)
        except KeyboardInterrupt:
            os.system(CLEAR)
            os.system(exit())
        except Exception as e:
            print_menu()
            print("[bold red]❌内部错误：[/bold red]{}".format(e))


if __name__ == "__main__":
    main("config.yaml")
