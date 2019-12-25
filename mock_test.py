# -*- coding:utf-8 -*-
from flask import *
import pymysql
import configparser

app = Flask(__name__)

#读取配置文件
def getconfig():
    cf = configparser.ConfigParser()
    path = 'db.ini'
    cf.read(path,encoding='UTF-8')
    dbhost={}
    dbhost['host'] = cf['database']['host']
    dbhost['user']  = cf['database']['user']
    dbhost['password']  =cf['database']['password']
    dbhost['dbname']  = cf['database']['dbname']
    return dbhost


@app.route('/<path:path>', methods=['GET','POST','PUT','DELETE'])
def mock(path):
    url = '/' + path
    methods = request.method
    method = methods.lower()
    dbhost = getconfig()
    host = dbhost['host']
    user = dbhost['user']
    password = dbhost['password']
    dbname = dbhost['dbname']
    try:
        db = pymysql.connect(host,user,password,dbname)
        query = db.cursor()
        sql_query = "select resparams from mock_config where url=%s and status=0 and methods=%s"
        query.execute(sql_query,(url, method))
        rows = query.execute(sql_query,(url, method))
        if rows==1:
            res = query.fetchone()[0]
            res = json.loads(res)
        else:
            data = '{"code": -1,"msg":"数据没有查询到,可能是methods方法不对"}'
            res = json.loads(data)
        db.close()
    except:
        data ='{"code": -1,"msg":"数据查询有误"}'
        res = json.loads(data)
    return res

@app.route('/<path:path>/<int:num>', methods=['GET','POST','PUT','DELETE'])
def mock2(path,num):
    url = '/'+path+'/'+"{num}"
    methods = request.method
    method = methods.lower()
    dbhost = getconfig()
    host = dbhost['host']
    user = dbhost['user']
    password = dbhost['password']
    dbname = dbhost['dbname']
    try:
        db = pymysql.connect(host,user,password,dbname)
        query = db.cursor()
        sql_query = "select resparams from mock_config where url=%s and status=0 and methods=%s"
        query.execute(sql_query,(url, method))
        rows = query.execute(sql_query,(url, method))
        if rows==1:
            res = query.fetchone()[0]
            res = json.loads(res)
        else:
            data = '{"code": -1,"msg":"数据没有查询到,可能是methods方法不对"}'
            res = json.loads(data)
        db.close()
    except:
        data ='{"code": -1,"msg":"数据查询有误"}'
        res = json.loads(data)
    return res

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8888)