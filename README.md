# 自动化利用谷歌搜索语法检测sql注入工具

使用sqlmapApi和yagooglesearch

需要在lib/link_conf.py中设置sqlmapApi的地址

## 开始使用

`pip install -r requeriment.txt`

**确保sqlmapApi已开启并且在link_conf.py中正确设置**
**确保能够访问google**

使用命令
```
set ...
    google:
        set google query <query> google查询关键字
        set google max_result_return <number> 最大返回条数(max 400)
        set google proxy <proxy> google代理
        set google query_file 关键字文件
        set save vulner_url <file> 保存漏洞url到文件
```
