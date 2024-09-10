# -*- coding: UTF-8 -*-
"""
@File    ：link_conf.py
@Author  ：Svanur
@Date    ：2024/9/8 17:45 
"""

# from sqlmapApi_v2.SqlmapClient.conf import HOST
# 服务端配置
IP = "192.168.3.15"
PORT = "8775"
HOST = "http://" + IP + ":" + PORT


class LinkConf:
    def __init__(self, url, method="GET", need_task=True, need_token=False, params=None):
        if params is None:
            params = dict()
        self.url = HOST + url
        self._url = self.url
        self.method = method
        self.need_task = need_task
        self.need_token = need_token
        self.task_id = None
        self.token = None
        self.params = params

    def get_link(self):
        if self.need_task and self.task_id is None:
            raise AttributeError("task_id is None")
        elif self.need_token and self.token is None:
            raise AttributeError("token is None")
        elif self.method == "POST" and self.params is None:
            raise AttributeError("params is None")
        return self.to_dict()

    def to_dict(self):
        return {
            "url": self.url,
            "method": self.method,
            "need_task": self.need_task,
            "need_token": self.need_token,
            "task_id": self.task_id,
            "token": self.token,
            "params": self.params
        }

    def set_token(self, token):
        self.token = token
        self.url = self.url.replace("<token>", token)

    def set_task(self, task_id):
        self.task_id = task_id
        self._url = self.url.replace("<taskid>", self.task_id)

    def set_params(self, params):
        self.params = params

    def get_url(self):
        return self._url

    def get_method(self):
        return self.method

    def get_need_token(self):
        return self.need_token

    def get_need_task_id(self):
        return self.need_task
