# -*- coding:utf-8 -*-
from flask import *
import pymysql
import datetime
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

# 首页
@app.route('/index.html')
def index():
    return render_template('index.html')

# 跳转到首页
@app.route('/')
def toindex():
    return render_template('index.html')

# 点击添加按钮，弹出页
@app.route('/add_mock')
def add_mock():
    return render_template('add_mock.html')

# 点击编辑按钮，弹出页
@app.route('/edit_mock')
def edit_mock():
    return render_template('edit_mock.html')

# 首页获取动态表格数据接口
@app.route('/code/mock/test/', methods=['GET'])
def api():
    page = int(request.args.get("page"))
    limit = int(request.args.get("limit"))
    pagenum = (page-1)*limit
    dbhost = getconfig()
    host = dbhost['host']
    user = dbhost['user']
    password = dbhost['password']
    dbname = dbhost['dbname']
    try:
        db = pymysql.connect(host,user,password,dbname)
        query1 = db.cursor()
        query2 = db.cursor()
        sql_query = "select id,title,methods,url,description,resparams,update_time from `mock_config` where `status`=0 order by update_time desc limit %s,%s"%(pagenum,limit)
        sql_count = "select count(id) from `mock_config` where `status`=0"
        query1.execute(sql_query)
        query2.execute(sql_count)
        num = query2.fetchone()[0]
        num2 = query1.execute(sql_query)
        results = query1.fetchall()
        list = []
        for i in range(0, num2, 1):
            id = results[i][0]
            title = results[i][1]
            methods = results[i][2]
            url = results[i][3]
            description = results[i][4]
            resparams = results[i][5]
            update_time = results[i][6]
            str_date = update_time.strftime('%Y-%m-%d %H:%M:%S')
            dict = {"id": id, "title": title, "methods": methods, "url": url, "description": description,
                    "resparams": resparams, "update_time": str_date}
            list.append(dict)
            sql_result = json.dumps({
                "code": 0,
                "msg": "",
                "count": num,
                "data": list
            }, ensure_ascii=False)
    except:
        print("Error: 数据还在火星")
        sql_result = json.dumps({
            "code": -2,
            "msg": "数据还在火星",
        }, ensure_ascii=False)
    db.close()
    return sql_result

# 点击删除按钮，接收ajax，进行数据处理
@app.route('/del', methods=['GET'])
def delmock():
    mockid = request.args.get("id")
    dbhost = getconfig()
    host = dbhost['host']
    user = dbhost['user']
    password = dbhost['password']
    dbname = dbhost['dbname']
    db = pymysql.connect(host,user,password,dbname)
    delect = db.cursor()
    sql = "update mock_config set `status`=1 where id = %s" % mockid
    try:
        delect.execute(sql)  # 执行SQL语句
        db.commit()  # 提交到数据库执行
        result = {'status': 0}
        del_result = json.dumps(result)
    except:
        db.rollback()  # 发生错误时回滚
    # 关闭数据库连接
    db.close()

    return del_result

# 点击确认添加按钮，接收ajax，进行数据处理
@app.route('/add', methods=['POST'])
def addmock():
    mockdata = json.loads(request.get_data())
    title = mockdata.get("title")
    methods = mockdata.get("methods")
    url = mockdata.get("url")
    description = mockdata.get("description")
    resparams = mockdata.get("resparams")
    status = 0
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %X")
    dbhost = getconfig()
    host = dbhost['host']
    user = dbhost['user']
    password = dbhost['password']
    dbname = dbhost['dbname']
    db = pymysql.connect(host, user, password, dbname)
    add = db.cursor()
    sql = "INSERT INTO mock_config(title,methods,url,description,update_time,resparams,status) VALUES ('%s','%s','%s','%s','%s','%s',%s)" %(title,methods,url,description,update_time,resparams,status)
    try:
        add.execute(sql)  # 执行SQL语句
        db.commit()  # 提交到数据库执行
        result = {'status': 0}
        add_result = json.dumps(result)
    except:
        db.rollback()  # 发生错误时回滚
    # 关闭数据库连接
    db.close()
    return add_result

# 点击确认修改按钮，接收ajax，进行数据处理
@app.route('/edit', methods=['POST'])
def editmock():
    mockdata = json.loads(request.get_data())
    id = mockdata.get("id")
    title = mockdata.get("title")
    methods = mockdata.get("methods")
    url = mockdata.get("url")
    description = mockdata.get("description")
    resparams = mockdata.get("resparams")
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %X")
    dbhost = getconfig()
    host = dbhost['host']
    user = dbhost['user']
    password = dbhost['password']
    dbname = dbhost['dbname']
    db = pymysql.connect(host, user, password, dbname)
    add = db.cursor()
    sql = "update mock_config set title='%s',methods='%s',url='%s',description='%s',update_time='%s',resparams='%s' where id=%s" %(title,methods,url,description,update_time,resparams,id)
    try:
        add.execute(sql)  # 执行SQL语句
        db.commit()  # 提交到数据库执行
        result = {'status': 0}
        edit_result = json.dumps(result)
    except:
        db.rollback()  # 发生错误时回滚
    # 关闭数据库连接
    db.close()
    return edit_result


if __name__ == '__main__':
    app.run()
