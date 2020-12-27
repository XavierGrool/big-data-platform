from flask import Blueprint, request
import json

import logging
LOG_FORMAT = "/********** %(asctime)s - %(levelname)s - %(message)s **********/"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

bp = Blueprint('help', __name__, url_prefix='/help')

# 获取帮助文档
@bp.route('/', methods = ['GET'])
def help():
    f = open("/root/app/big_data/resources/help.md", "r")
    content = f.read()
    f.close()
    return {"content": content}