from flask import Blueprint, request
from big_data.db import get_db, close_db
import json

import logging
LOG_FORMAT = "/********** %(asctime)s - %(levelname)s - %(message)s **********/"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

bp = Blueprint('model', __name__, url_prefix='/model')

# 获取所有模型
@bp.route('get-all/', methods = ['POST'])
def getAll():
    # 变量初始化 & 接收请求数据
    status = 0
    total = 0
    models = []
    received_data = request.get_json(silent=True)

    # logging
    logging.info("received_data: " + json.dumps(received_data))

    # 应该接收到有:
    # project_id, num, start[not index]
    project_id = received_data['project_id']
    num = received_data['num']
    start = received_data['start']

    # 获取 total[not index]
    db = get_db()
    c = db.cursor()
    t = (project_id,)
    c.execute("SELECT COUNT(*) FROM model WHERE project_id=?", t)
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
        t = (project_id, start - 1, num)
        key = 0
        tmp = {
            "id": 0,
            "key": "",
            "name": "",
            "description": ""
        }
        for model in c.execute("SELECT * FROM model WHERE project_id=? LIMIT ?, ?", t):
            logging.info(tuple(model))
            tmp["id"] = tuple(model)[0]
            key = key + 1
            tmp["key"] = str(key)
            tmp["name"] = tuple(model)[2]
            tmp_description = tuple(model)[3]
            if tmp_description == "":
                tmp_description = "无"
            tmp["description"] = tmp_description
            models.append(tmp.copy())
        logging.info(models)

    close_db()

    # 接口约定:
    # status: 状态码
    # total: 总模型数
    # models: 模型数组
    return {
        "status": status,
        "total": total,
        "models": models
    }