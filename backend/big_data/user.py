from flask import Blueprint, request
from big_data.db import get_db, close_db
import json

import logging
LOG_FORMAT = "/********** %(asctime)s - %(levelname)s - %(message)s **********/"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

bp = Blueprint('user', __name__, url_prefix='/user')

# 获取用户信息
@bp.route('info/', methods = ['POST'])
def info():
    # 变量初始化 & 接收请求数据
    status = 0
    received_data = request.get_json(silent=True)

    # logging
    logging.info("received_data: " + json.dumps(received_data))

    # 查询数据库
    db = get_db()
    c = db.cursor()
    t = (received_data['username'],)
    c.execute("SELECT * FROM user WHERE username=?", t)
    res = c.fetchone()
    if res == None: # 用户不存在
        logging.info("no results") # logging
        status = 0
    else:           # 用户存在
        logging.info(tuple(res))   # logging
        status = 1
        if tuple(res)[3] == 16: # 超级管理员
            role = 1
        else:                   # 普通用户
            role = 2
    close_db()

    # 接口约定：
    # 状态码:
    #     0: 用户不存在  1: 用户存在
    # 用户身份:
    #     1: 超级管理员  2: 普通用户
    return {
        "status": status,
        "username": received_data['username'],
        "role": role
    }

# 修改密码
@bp.route('change-passwd/', methods = ['POST'])
def changePasswd():
    # 变量初始化 & 接收请求数据
    status = 0
    received_data = request.get_json(silent=True)

    # logging
    logging.info("received_data: " + json.dumps(received_data))

    # 接收到的有 username, old_passwd, new_passwd
    # 首先判断一下 old_passwd 对不对
    # 不对则返回状态码 0
    # 对的话更新数据库中的 password 字段，然后返回状态码 1

    # 更新算法
    db = get_db()
    c = db.cursor()
    t = (received_data['username'],)
    c.execute("SELECT password FROM user WHERE username=?", t)
    res = c.fetchone()
    if received_data['old_passwd'] != tuple(res)[0]: # 旧密码验证失败
        logging.info("密码验证失败") # logging
        status = 0
    else:                                            # 旧密码验证成功
        logging.info("密码验证成功") # logging
        t = (received_data['new_passwd'], received_data['username'])
        c.execute("UPDATE user SET password=? WHERE username=?", t)
        db.commit()
        status = 1
    close_db()

    # 接口约定:
    # 状态码:
    # 0: 旧密码验证失败  1: 修改密码成功
    return {"status": status}

# 添加用户
@bp.route('add/', methods = ['POST'])
def add():
    # 变量初始化 & 接收请求数据
    status = 0
    received_data = request.get_json(silent=True)

    # logging
    logging.info("received_data: " + json.dumps(received_data))

    # 接收到的数据有:
    # username, passwd, permission
    username = received_data['username']
    passwd = received_data['passwd']
    permission = received_data['permission']

    # 普通用户的权限为 0-15
    if permission < 0 or permission > 15:
        status = 0
    else:
        status = 1
        db = get_db()
        c = db.cursor()
        t = (username, passwd, permission)
        c.execute("INSERT INTO user (username, password, permission) VALUES (?, ?, ?)", t)
        db.commit()
        close_db()
    
    # 接口约定:
    # 状态码:
    # 0: 添加失败  1: 添加成功
    return {"status": status}

# 删除单个用户
@bp.route('delete/one/', methods = ['POST'])
def deleteOne():
    # 变量初始化 & 接收请求数据
    status = 0
    received_data = request.get_json(silent=True)

    # logging
    logging.info("received_data: " + json.dumps(received_data))

    # 接收到的数据有:
    # id
    id = received_data['id']

    db = get_db()
    c = db.cursor()
    t = (str(id),)
    c.execute("DELETE FROM user WHERE id=?", t)
    db.commit()
    status = 1
    close_db()

    # 接口约定:
    # 0: 删除失败  1: 删除成功
    return {"status": status}

# 删除一些用户
@bp.route('delete/some/', methods = ['POST'])
def deleteSome():
    # 变量初始化 & 接收请求数据
    status = 0
    received_data = request.get_json(silent=True)

    # logging
    logging.info("received_data: " + json.dumps(received_data))

    # 接收到的数据有:
    # ids
    ids = received_data['ids']

    db = get_db()
    c = db.cursor()
    for id in ids:
        t = (str(id),)
        c.execute("DELETE FROM user WHERE id=?", t)
        db.commit()

    status = 1
    close_db()

    # 接口约定:
    # 0: 删除失败  1: 删除成功
    return {"status": status}

# 获取所有用户
@bp.route('get-all/', methods = ['POST'])
def getAllUsers():
    # 变量初始化 & 接收请求数据
    status = 0
    total = 0
    users = []
    received_data = request.get_json(silent=True)

    # logging
    logging.info("received_data: " + json.dumps(received_data))

    # 应该接收到有:
    # num, start[not index]
    num = received_data['num']
    start = received_data['start']

    # 获取 total[not index]
    db = get_db()
    c = db.cursor()
    c.execute("SELECT COUNT(*) FROM user")
    res = c.fetchone()
    total = tuple(res)[0]

    # 如果 start > total
    #   返回状态码为 0
    # 如果 start <= total
    #   返回 num 个用户信息
    if start > total:
        status = 0
    else:
        status = 1
        t = (start - 1, num)
        key = 0
        tmp = {
            "id": 0,
            "key": "",
            "name": "",
            "permission": ['nice', 'developer']
        }
        for user in c.execute("SELECT * FROM user LIMIT ?, ?", t):
            logging.info(tuple(user))
            tmp["id"] = tuple(user)[0]
            key = key + 1
            tmp["key"] = str(key)
            tmp["name"] = tuple(user)[1]
            users.append(tmp.copy())
        logging.info(users)

    close_db()

    # 接口约定:
    # status: 状态码
    # total: 总用户数
    # users: 用户信息数组
    return {
        "status": status,
        "total": total,
        "users": users
    }
