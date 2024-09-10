# -*- coding: UTF-8 -*-
"""
@File    ：google.py
@Author  ：Svanur
@Date    ：2024/9/3 15:24 
"""
from enum import Enum
import yagooglesearch
from colorama import *


class MessageType(Enum):
    FAILED = 0
    SUCCESS = 1
    INFO = 2


def google_search(query, tbs="li:1", max_result_return=10, http_cool_time=10, http_cool_factor=1.5,
                  proxy="http://127.0.0.1:7890", verbosity=1, verbose_output=True):
    """
    :param query: 要搜索的关键字
    :param tbs:
    :param max_result_return: 最大返回条数
    :param http_cool_time: 封禁冷却时间
    :param http_cool_factor: 封禁冷却时间倍数
    :param proxy: 代理
    :param verbosity: 日志打印相关
    :param verbose_output: True: 返回详细结果 False: 只返回url
    :return:
    """
    client = yagooglesearch.SearchClient(
        query,
        tbs=tbs,
        max_search_result_urls_to_return=max_result_return,
        http_429_cool_off_time_in_minutes=http_cool_time,
        http_429_cool_off_factor=http_cool_factor,
        proxy=proxy,
        verbosity=verbosity,
        verbose_output=verbose_output
    )
    client.assign_random_user_agent()
    return client.search()


def show_message(msg, type=MessageType.INFO):
    color = None
    start_str = ""
    if type == MessageType.SUCCESS:
        color = Fore.GREEN
        start_str = "✔"
    elif type == MessageType.FAILED:
        color = Fore.RED
        start_str = "✘"
    elif type == MessageType.INFO:
        color = Fore.BLUE
        start_str = "ℹ"
    print(color + f"[{start_str}] " + Fore.RESET + msg)

