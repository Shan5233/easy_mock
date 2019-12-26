Easy Mock 是一个可视化，并且能快速生成模拟数据的持久化服务。基于python flask框架，结合layui、mysql等打造。

mockserver_setting.py、mockweb_setting.py以及run、logs文件夹为gunicorn配置所需。

以下是gunicorn在linux中的启动命令：

nohup gunicorn -c mockweb_setting.py mockweb:app &
nohup gunicorn -c mockserver_setting.py mockserver:app &