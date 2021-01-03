from flask import Blueprint, request
from big_data.db import get_db, close_db
import json

import logging
LOG_FORMAT = "/********** %(asctime)s - %(levelname)s - %(message)s **********/"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

bp = Blueprint('project', __name__, url_prefix='/project')

# 添加项目
@bp.route('add/', methods = ['POST'])
def add():
    # 变量初始化 & 接收请求数据
    status = 0
    received_data = request.get_json(silent=True)

    # logging
    logging.info("received_data: " + json.dumps(received_data))

    # 接收到的数据有:
    # username, name, description
    username = received_data['username']
    name = received_data['name']
    description = received_data['description']

    # 插入数据库
    db = get_db()
    c = db.cursor()
    t = (username, name, description)
    c.execute("INSERT INTO project (username, name, description) VALUES (?, ?, ?)", t)
    db.commit()
    status = 1
    close_db()

    # 接口约定:
    # 状态码:
    # 0: 添加失败  1: 添加成功
    return {"status": status}

# 获取所有项目
@bp.route('get-all/', methods = ['POST'])
def getAllProjects():
    # 变量初始化 & 接收请求数据
    status = 0
    total = 0
    projects = []
    received_data = request.get_json(silent=True)

    # logging
    logging.info("received_data: " + json.dumps(received_data))

    # 应该接收到有:
    # username, num, start[not index]
    username = received_data['username']
    num = received_data['num']
    start = received_data['start']

    # 获取 total[not index]
    db = get_db()
    c = db.cursor()
    t = (username,)
    c.execute("SELECT COUNT(*) FROM project WHERE username=?", t)
    res = c.fetchone()
    total = tuple(res)[0]

    # 如果 start > total
    #   返回状态码为 0
    # 如果 start <= total
    #   返回 num 个项目信息
    if start > total:
        status = 0
    else:
        status = 1
        t = (username, start - 1, num)
        key = 0
        tmp = {
            "id": 0,
            "key": "",
            "name": "",
            "description": ""
        }
        for project in c.execute("SELECT * FROM project WHERE username=? LIMIT ?, ?", t):
            logging.info(tuple(project))
            tmp["id"] = tuple(project)[0]
            key = key + 1
            tmp["key"] = str(key)
            tmp["name"] = tuple(project)[2]
            tmp_description = tuple(project)[3]
            if tmp_description == "":
                tmp_description = "无"
            tmp["description"] = tmp_description
            projects.append(tmp.copy())
        logging.info(projects)

    close_db()

    # 接口约定:
    # status: 状态码
    # total: 总项目数
    # projects: 项目数组
    return {
        "status": status,
        "total": total,
        "projects": projects
    }

# 获取项目名称
@bp.route('get-name/', methods = ['POST'])
def getName():
    # 变量初始化 & 接收请求数据
    status = 0
    name = ""
    received_data = request.get_json(silent=True)

    # logging
    logging.info("received_data: " + json.dumps(received_data))

    # 接收到的数据有:
    # id
    id = received_data['id']

    # 在数据库查找
    db = get_db()
    c = db.cursor()
    t = (id,)
    c.execute("SELECT name FROM project WHERE id=?", t)
    res = c.fetchone()
    name = tuple(res)[0]
    status = 1
    close_db()

    # 接口约定:
    return {
        "status": status,
        "name": name
    }
