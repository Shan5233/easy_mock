# -*- coding:utf-8 -*-
from flask import *
import pymysql
import datetime
import configparser
from DBUtils.PooledDB import PooledDB

app = Flask(__name__)


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
    pagenum = (page - 1) * limit
    try:
        conn = pool.connection()
        query1 = conn.cursor()
        query2 = conn.cursor()
        sql_query = "select id,title,methods,url,description,resparams,update_time from `mock_config` where `status`=0 order by update_time desc limit %s,%s" % (
        pagenum, limit)
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
        query1.close()
        query2.close()
        conn.close()
    except:
        print("Error: 数据还在火星")
        sql_result = json.dumps({
            "code": -2,
            "msg": "数据还在火星",
        }, ensure_ascii=False)
    return sql_result


# 点击删除按钮，接收ajax，进行数据处理
@app.route('/del', methods=['GET'])
def delmock():
    mockid = request.args.get("id")
    conn = pool.connection()
    delect = conn.cursor()
    sql = "update mock_config set `status`=1 where id = %s" % mockid
    try:
        delect.execute(sql)  # 执行SQL语句
        conn.commit()  # 提交到数据库执行
        result = {'status': 0}
        del_result = json.dumps(result)
    except:
        conn.rollback()  # 发生错误时回滚
    # 关闭数据库连接
    delect.close()
    conn.close()
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
    conn = pool.connection()
    add = conn.cursor()
    sql = "INSERT INTO mock_config(title,methods,url,description,update_time,resparams,status) VALUES ('%s','%s','%s','%s','%s','%s',%s)" % (
    title, methods, url, description, update_time, resparams, status)
    try:
        add.execute(sql)  # 执行SQL语句
        conn.commit()  # 提交到数据库执行
        result = {'status': 0}
        add_result = json.dumps(result)
    except:
        conn.rollback()  # 发生错误时回滚
    # 关闭数据库连接
    add.close()
    conn.close()
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
    conn = pool.connection()
    edit = conn.cursor()
    sql = "update mock_config set title='%s',methods='%s',url='%s',description='%s',update_time='%s',resparams='%s' where id=%s" % (
    title, methods, url, description, update_time, resparams, id)
    try:
        edit.execute(sql)  # 执行SQL语句
        conn.commit()  # 提交到数据库执行
        result = {'status': 0}
        edit_result = json.dumps(result)
    except:
        conn.rollback()  # 发生错误时回滚
    # 关闭数据库连接
    edit.close()
    conn.close()
    return edit_result


if __name__ == '__main__':
    app.run()
