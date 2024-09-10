# -*- coding: UTF-8 -*-
"""
@File    ：goosql.py
@Author  ：Svanur
@Date    ：2024/9/8 22:03 
"""
import cmd
import threading
import time
from queue import Queue

from lib.engine import Engine
from lib.tools import google_search, show_message, MessageType


class GooSql(cmd.Cmd):
    def __init__(self):
        self.prompt = "gooSql>"
        super().__init__()
        self.engine = None
        self.google_conf = {
            "query": "Hellow World",
            "tbs": "li:1",
            "max_result_return": 10,
            "http_cool_time": 10,
            "http_cool_factor": 1.5,
            "proxy": "http://127.0.0.1:7890",
            "verbosity": 1,
            "verbose_output": True
        }
        self.file_conf = "keywords.txt"
        self.init()
        self.urls = Queue(maxsize=200)
        self.vulner_urls = Queue(maxsize=200)
        self.save_vulner_file = "vulner.txt"
        self.google_tasks_lock = threading.Semaphore(2)
        self.urls_lock = threading.Lock()
        self.tmp_vulner = set()

    def init(self):
        print("""                                                                                                    
   ____            _                                            _   _     _          ____                           _        
 / ___|    __ _  | |  _ __ ___     __ _   _ __     __      __ (_) | |_  | |__      / ___|   ___     ___     __ _  | |   ___ 
 \___ \   / _` | | | | '_ ` _ \   / _` | | '_ \    \ \ /\ / / | | | __| | '_ \    | |  _   / _ \   / _ \   / _` | | |  / _ \\
  ___) | | (_| | | | | | | | | | | (_| | | |_) |    \ V  V /  | | | |_  | | | |   | |_| | | (_) | | (_) | | (_| | | | |  __/
 |____/   \__, | |_| |_| |_| |_|  \__,_| | .__/      \_/\_/   |_|  \__| |_| |_|    \____|  \___/   \___/   \__, | |_|  \___|
             |_|                         |_|                                                               |___/     
        """)
        show_message("连接SqlmapApi中...", MessageType.INFO)
        self.engine = Engine()
        show_message("测试谷歌搜索模块中...")
        try:
            res = google_search(**self.google_conf)
            if res:
                show_message("测试成功", MessageType.SUCCESS)
        except Exception as e:
            show_message("谷歌搜索模块测试失败...\n" + str(e), MessageType.FAILED)
            exit(-1)

    def emptyline(self):
        pass

    def load_file(self):
        if self.file_conf == "":
            show_message("not select file [set google query_file <file_name>]", MessageType.FAILED)
            return []
        try:
            data = open(self.file_conf, "r").read()
            queries = data.split("\n")
            show_message("file load success", MessageType.SUCCESS)
            return queries
        except Exception as e:
            show_message("file load failed: " + str(e.args[-1]), MessageType.FAILED)
            return []

    def google_search(self):
        return google_search(**self.google_conf)

    def load_method(self, method_head_name, arg):
        args = arg.split(" ")
        method = ""
        if method_head_name == "set":
            try:
                method = f"{method_head_name}_{args[0]}_{args[1]}"
                _arg = args[2]
            except IndexError:
                show_message("command error", MessageType.FAILED)
                return
            m = getattr(self, method)
            if callable(m):
                m(_arg)
        elif method_head_name == "show":
            method = f"{method_head_name}_{args[0]}_{args[1]}"
            m = getattr(self, method)
            if callable(m):
                m()

    def do_set(self, arg):
        """set ...
            google:
                set google query <query> google查询关键字
                set google max_result_return <number> 最大返回条数(max 400)
                set google proxy <proxy> google代理
                set google query_file 关键字文件
            set save vulner_url <file> 保存漏洞url到文件
        """
        self.load_method("set", arg)

    def set_google_query(self, arg):
        self.google_conf["query"] = arg
        show_message("设置成功", MessageType.SUCCESS)

    def set_google_max_result_return(self, arg):
        if int(arg) > 400 or int(arg) < 1:
            show_message("max_result_return out of range", MessageType.FAILED)
            return
        self.google_conf["max_result_return"] = int(arg)
        show_message("设置成功", MessageType.SUCCESS)

    def set_google_proxy(self, arg):
        self.google_conf["proxy"] = arg
        show_message("设置成功", MessageType.SUCCESS)

    def set_google_query_file(self, arg):
        self.file_conf = arg
        show_message("设置成功", MessageType.SUCCESS)

    def set_save_vulner_file(self, arg):
        self.save_vulner_file = arg
        show_message("设置成功", MessageType.SUCCESS)

    def do_google(self, arg):
        res = self.google_search()
        for item in res:
            self.urls.put(item["url"], block=True)

    def do_show(self, arg):
        self.load_method("show", arg)

    def show_google_conf(self):
        for key, value in self.google_conf.items():
            print(f"\t{key}:\t{value}")
        print(f"\tgoogle_query_file:\t{self.file_conf}")

    def show_google_urls(self):
        urls = list(self.urls.queue)
        show_message(f"google urls' num is {len(urls)}")

    def do_help(self, arg):
        super().do_help(arg)

    def do_EOF(self):
        print("bye~")

    def sqlmap(self, url):
        self.engine.start_scan({"url": url})

    def get_vulner_urls(self):
        for url in self.engine.get_vulner_url():
            if url not in self.tmp_vulner:
                show_message(f"{url}", MessageType.SUCCESS)
                self.vulner_urls.put(url, block=True)
                self.tmp_vulner.add(url)
                self.save_vulner_urls(url)
        show_message(f"vulner url num: {len(self.tmp_vulner)}", MessageType.SUCCESS)

    def save_vulner_urls(self,url):
        if self.save_vulner_file != "":
            try:
                f = open(self.save_vulner_file, "a+")
                f.write(url + "\n")
            except Exception as e:
                show_message(f"save failed: {e.args[-1]}", MessageType.FAILED)

    def do_start(self, arg):
        """start 开始自动化sqlmap检测"""
        show_message("loading file...")
        keywords = self.load_file()
        if not keywords:
            return
        threading.Thread(target=self.detecting).start()
        for keyword in keywords:
            self.google_tasks_lock.acquire()
            threading.Thread(target=self.auto_submit, args=(keyword,)).start()

    def auto_submit(self, keyword):
        query = keyword
        max_result_return = self.google_conf["max_result_return"]
        proxy = self.google_conf["proxy"]
        res = google_search(query, max_result_return=max_result_return, proxy=proxy)
        for item in res:
            self.urls.put(item["url"], block=True)
        self.google_tasks_lock.release()

    def detecting(self):

        while True:
            time.sleep(3)
            tasks = self.engine.get_all_task()
            count = 0
            if tasks['success']:
                for key, value in tasks['tasks'].items():
                    if value == "running":
                        count += 1
            _count = count
            while count < 10:
                self.engine.scan(self.urls.get(block=True))
                count += 1
            if _count != 10:
                show_message(f"has submit {count - _count} tasks, url list num {len(self.urls.queue)}")
            self.get_vulner_urls()


if __name__ == '__main__':
    goosql = GooSql()
    goosql.cmdloop()
