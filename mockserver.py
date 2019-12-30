# -*- coding:utf-8 -*-
from flask import *
import pymysql
import configparser
from DBUtils.PooledDB import PooledDB

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"


# 读取配置文件
def getconfig():
    cf = configparser.ConfigParser()
    path = 'db.ini'
    cf.read(path, encoding='UTF-8')
    dbhost = {}
    dbhost['host'] = cf['database']['host']
    dbhost['port'] = cf['database']['port']
    dbhost['user'] = cf['database']['user']
    dbhost['password'] = cf['database']['password']
    dbhost['dbname'] = cf['database']['dbname']
    return dbhost

# 数据库连接池
dbhost = getconfig()
host = dbhost['host']
port = int(dbhost['port'])
user = dbhost['user']
password = dbhost['password']
dbname = dbhost['dbname']
pool = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
    maxshared=3,
    # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    ping=0,
    # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    host=host,
    port=port,
    user=user,
    password=password,
    database=dbname,
    charset='utf8'
)


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def mock(path):
    url = '/' + path
    methods = request.method
    method = methods.lower()
    try:
        conn = pool.connection()
        query = conn.cursor()
        sql_query = "select resparams from mock_config where url=%s and status=0 and methods=%s"
        query.execute(sql_query, (url, method))
        rows = query.execute(sql_query, (url, method))
        if rows == 1:
            data = query.fetchone()[0]
            data_dict = json.loads(data)
            res = jsonify(data_dict)
        else:
            data = {"code": -1, "msg": "数据没有查询到,可能是methods方法不对"}
            res = jsonify(data)
        query.close()
        conn.close()
    except:
        data = {"code": -1, "msg": "数据查询有误"}
        res = jsonify(data)
    return res


@app.route('/<path:path>/<int:num>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def mock2(path, num):
    url = '/' + path + '/' + "{num}"
    methods = request.method
    method = methods.lower()
    try:
        conn = pool.connection()
        query = conn.cursor()
        sql_query = "select resparams from mock_config where url=%s and status=0 and methods=%s"
        query.execute(sql_query, (url, method))
        rows = query.execute(sql_query, (url, method))
        if rows == 1:
            data = query.fetchone()[0]
            data_dict = json.loads(data)
            res = jsonify(data_dict)
        else:
            data = {"code": -1, "msg": "数据没有查询到,可能是methods方法不对"}
            res = jsonify(data)
        query.close()
        conn.close()
    except:
        data = {"code": -1, "msg": "数据查询有误"}
        res = jsonify(data)
    return res


if __name__ == '__main__':
    app.run()
