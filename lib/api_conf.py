# -*- coding: UTF-8 -*-
"""
@File    ：conf.py
@Author  ：Svanur
@Date    ：2024/9/8 17:47 
"""
from lib.link_conf import LinkConf


# 辅助
CREATE_NEW_TASK = LinkConf("/task/new", need_task=False)
DELETE_TASK = LinkConf("/task/<taskid>/delete")
# Admin
GET_ALL_TASK = LinkConf("/admin/list", need_task=False)
DELETE_ALL_TASK = LinkConf("/admin/flush", need_task=False)

# 核心交互
LIST_TASK_OPTION = LinkConf("/option/<taskid>/list")
SET_TASK_OPTION = LinkConf("/option/<taskid>/set", method="POST", params={'a': 2})

START_SCAN = LinkConf("/scan/<taskid>/start", method="POST")
STOP_SCAN = LinkConf("/scan/<taskid>/stop")
STATUS_SCAN = LinkConf("/scan/<taskid>/status")
DATA_SCAN = LinkConf("/scan/<taskid>/data")
LOG_SCAN = LinkConf("/scan/<taskid>/log")
KILL_SCAN = LinkConf("/scan<taskid>/kill")
