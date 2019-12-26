# -*- coding:utf-8 -*-
from flask import *
import pymysql
import configparser

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] ="application/json;charset=utf-8"

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


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def mock(path):
    url = '/' + path
    methods = request.method
    method = methods.lower()
    dbhost = getconfig()
    host = dbhost['host']
    port = int(dbhost['port'])
    user = dbhost['user']
    password = dbhost['password']
    dbname = dbhost['dbname']
    try:
        db = pymysql.connect(host=host, user=user, password=password, db=dbname, port=port)
        query = db.cursor()
        sql_query = "select resparams from mock_config where url=%s and status=0 and methods=%s"
        query.execute(sql_query, (url, method))
        rows = query.execute(sql_query, (url, method))
        if rows == 1:
            data = query.fetchone()[0]
            data_dict = json.loads(data)
            res = jsonify(data_dict)
        else:
            data = {"code": -1,"msg": "数据没有查询到,可能是methods方法不对"}
            res = jsonify(data)
        db.close()
    except:
        data = {"code": -1,"msg":"数据查询有误"}
        res = jsonify(data)
    return res


@app.route('/<path:path>/<int:num>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def mock2(path, num):
    url = '/' + path + '/' + "{num}"
    methods = request.method
    method = methods.lower()
    dbhost = getconfig()
    host = dbhost['host']
    port = int(dbhost['port'])
    user = dbhost['user']
    password = dbhost['password']
    dbname = dbhost['dbname']
    try:
        db = pymysql.connect(host=host, user=user, password=password, db=dbname, port=port)
        query = db.cursor()
        sql_query = "select resparams from mock_config where url=%s and status=0 and methods=%s"
        query.execute(sql_query, (url, method))
        rows = query.execute(sql_query, (url, method))
        if rows == 1:
            data = query.fetchone()[0]
            data_dict = json.loads(data)
            res = jsonify(data_dict)
        else:
            data = {"code": -1,"msg":"数据没有查询到,可能是methods方法不对"}
            res = jsonify(data)
        db.close()
    except:
        data = {"code": -1,"msg":"数据查询有误"}
        res = jsonify(data)
    return res


if __name__ == '__main__':
    app.run()
