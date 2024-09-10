# -*- coding: UTF-8 -*-
"""
@File    ：engine.py
@Author  ：Svanur
@Date    ：2024/9/5 11:25 
"""

import requests
import json
from lib.link_conf import *
from lib.api_conf import *
from enum import Enum
from colorama import Fore, Style
from requests.exceptions import ConnectionError

from lib.tools import show_message, MessageType


class SqlmapResultType(Enum):
    RESULT_NEW_TASK = 0
    RESULT_ALL_TASKS = 1
    RESULT_TASK_STATUS = 2
    RESULT_TASK_DATA = 3
    RESULT_TASK_LOG = 4
    RESULT_VULNER_URL = 5


class Engine:
    def __init__(self):
        self.requests = requests
        self.init()

    def init(self):
        try:
            res = self.parser_object(GET_ALL_TASK)
            show_message("sqlmapApi连接成功", MessageType.SUCCESS)
        except ConnectionError as e:
            show_message("连接失败，请确认sqlmapApi服务状态", MessageType.FAILED)
            exit(-1)

    def parser_object(self, object, **kwargs):
        """
        解析配置类
        :param object:
        :param kwargs:
        :return:
        """
        assert type(object) is LinkConf, "object must is LinkConf"
        method = object.get_method()
        res = None
        if object.get_need_token():
            token = kwargs["token"]
            object.set_token(token)
        if object.get_need_task_id():
            task_id = kwargs["task_id"]
            object.set_task(task_id)
        url = object.get_url()
        if method == "POST":
            params = kwargs["params"]
            res = self.post_request(url, params)
        elif method == "GET":
            res = self.get_request(url)
        return res

    def get_request(self, url):
        """
        get 请求
        :param url:
        :return:
        """
        request = self.requests.get(url, timeout=3)
        if request.status_code == 200:
            result = request.json()
            request.close()
            return result
        else:
            return False

    def post_request(self, url, params):
        """
        post 请求
        :param url:
        :param params:
        :return:
        """
        headers = {
            "Content-Type": "application/json"
        }
        request = self.requests.post(url, headers=headers, data=json.dumps(params), timeout=3)
        result = request.json()
        request.close()
        return result

    def create_task(self):
        """
        创建一个新任务
        :return: 任务id
        """
        res = self.parser_object(CREATE_NEW_TASK)
        if res["success"]:
            return res["taskid"]

    def start_scan(self, task_id, params):
        """
        开始扫描
        :param task_id: 任务id
        :param params: 参数字典
        :return:
        """
        res = self.parser_object(START_SCAN, task_id=task_id, params=params)
        return res

    def scan(self, url):
        task_id = self.create_task()
        self.start_scan(task_id, {"url": url})

    def get_all_task(self):
        """
        获取全部的任务
        :return:
        """
        res = self.parser_object(GET_ALL_TASK)
        return res

    def clear_all_task(self):
        res = self.parser_object(DELETE_ALL_TASK)
        return res

    def kill_task(self, task_id):
        res = self.parser_object(KILL_SCAN, task_id=task_id)
        return res

    def get_task_status(self, task_id):
        res = self.parser_object(STATUS_SCAN, task_id=task_id)
        return res

    def get_task_data(self, task_id):
        res = self.parser_object(DATA_SCAN, task_id=task_id)
        return res

    def get_task_log(self, task_id):
        res = self.parser_object(LOG_SCAN, task_id=task_id)
        return res

    def stop_scan(self, task_id):
        res = self.parser_object(STOP_SCAN, task_id=task_id)
        return res

    def get_vulner_url(self):
        all_tasks = self.get_all_task()
        if all_tasks["success"]:
            for key in all_tasks["tasks"].keys():
                data = self.get_task_data(key)
                if data["success"]:
                    if data["data"]:
                        yield data["data"][0]["value"]["url"] + "/" + data["data"][0]["value"]["query"]
