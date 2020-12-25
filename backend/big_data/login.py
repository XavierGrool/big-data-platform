from flask import Blueprint, request
from big_data.db import get_db
import json

import logging
LOG_FORMAT = "/********** %(asctime)s - %(levelname)s - %(message)s **********/"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

bp = Blueprint('login', __name__, url_prefix='/login')

# 登录接口
@bp.route('/', methods = ['POST'])
def login():
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
    if res == None:
        logging.info("no results") # logging
        status = 0
    else:
        logging.info(tuple(res)) # logging
        if received_data['password'] == tuple(res)[2]:
            status = 1
        else:
            status = 2

    # 接口约定：
    # 0: 用户不存在  1: 登录成功  2: 密码错误
    return {"status": status}
