from flask import Blueprint, request
from big_data.db import get_db, close_db
import json, os
from big_data.spark import get_spark, get_client

import logging
LOG_FORMAT = "/********** %(asctime)s - %(levelname)s - %(message)s **********/"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

bp = Blueprint('dataset', __name__, url_prefix='/dataset')


class Dataset:
    def __init__(self, username, project_id, name, description, separator, columns, file_obj):
        self.username = username
        self.project_id = project_id
        self.name = name
        self.description = description
        self.separator = separator
        self.columns = columns
        self.file_obj = file_obj
        self.local_dir = os.getcwd() + "/"
        self.hdfs_dir = "/user/" + username + "/" + project_id + "/"

    def logging(self):
        logging.info("ds 的内容如下:")
        logging.info(self.username)
        logging.info(self.project_id)
        logging.info(self.name)
        logging.info(self.description)
        logging.info(self.separator)
        logging.info(self.columns)
        logging.info(self.file_obj)

    # 上传时的进度回调函数
    def uploadCallback(self, filename, size):
        print(filename, "one chunk uploaded, ", "current size: ", size)
        if size == -1:
            print("file uploaded")

    # 临时地把文件保存到本地
    def saveFileToLocal(self):
        self.file_obj.save(self.local_dir + self.file_obj.filename)

    # 删除本地临时文件
    def deleteLocalFile(self):
        os.remove(self.local_dir + self.file_obj.filename)

    # 把本地文件上传到 Hadoop
    def uploadToHadoop(self):
        get_client().upload(
            hdfs_path = self.hdfs_dir + self.file_obj.filename,
            local_path = self.local_dir + self.file_obj.filename,
            chunk_size = 2 << 19,
            progress = self.uploadCallback
        )

    # 删除 Hadoop 中该项目下的所有数据集
    def deleteAllFromHadoop(self):
        get_client().delete(self.hdfs_dir, recursive=True)

    # 删除 Hadoop 中该数据集的原始文件
    def deleteRawFromHadoop(self):
        get_client().delete(self.hdfs_dir + self.file_obj.filename)

    # 数据处理
    def dataProcess(self):
        # 数据初始化
        sc = get_spark().sparkContext
        separator = self.separator
        columns = self.columns

        # 读取数据集文件
        lines = sc.textFile(self.hdfs_dir + self.file_obj.filename)

        # 用分割符对行进行分割
        splits = lines.map(lambda x: x.split(separator))

        # 数据类型转换
        transformed = splits.map(lambda x: typeTransform(x, columns))
        
        # 创建 dataframe
        col_name = []
        for column in columns:
            col_name.append(column["col_name"])
        logging.info(col_name)
        df = get_spark().createDataFrame(transformed, col_name)

        # 这里改命名 parquet 文件的规则
        df.select("*").write.save(self.hdfs_dir + self.file_obj.filename.split(".")[0] + ".parquet")


# 数据类型转换
def typeTransform(x, columns):
    for i, column in enumerate(columns):
        if column["data_type"] == "1":
            x[i] = int(x[i])
        if column["data_type"] == "2":
            x[i] = float(x[i])
    return x

# 上传文件
@bp.route('upload/', methods = ['POST'])
def info():
    # 变量初始化 & 初始化数据集对象
    status = 0
    ds = Dataset(
        request.form['username'],
        request.form['project_id'],
        request.form['name'],
        request.form['description'],
        request.form['separator'],
        json.loads(request.form['columns']),
        request.files['file']
    )

    # logging
    ds.logging()

    # 
    ds.saveFileToLocal()
    ds.uploadToHadoop()
    ds.deleteLocalFile()
    ds.dataProcess()
    ds.deleteRawFromHadoop()
    # ds.deleteAllFromHadoop()

    # 插入数据库
    db = get_db()
    c = db.cursor()
    t = (int(ds.project_id), ds.name, ds.file_obj.filename.split(".")[0], ds.description)
    c.execute("INSERT INTO dataset (project_id, name, filename, description) VALUES (?, ?, ?, ?)", t)
    db.commit()
    status = 1
    close_db()

    # 接口约定:
    # 状态码:
    # 0: 添加失败  1: 添加成功
    return {"status": status}

# 获取所有数据集
@bp.route('get-all/', methods = ['POST'])
def getAllDatasets():
    # 变量初始化 & 接收请求数据
    status = 0
    total = 0
    datasets = []
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
    c.execute("SELECT COUNT(*) FROM dataset WHERE project_id=?", t)
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
        for dataset in c.execute("SELECT * FROM dataset WHERE project_id=? LIMIT ?, ?", t):
            logging.info(tuple(dataset))
            tmp["id"] = tuple(dataset)[0]
            key = key + 1
            tmp["key"] = str(key)
            tmp["name"] = tuple(dataset)[2]
            tmp_description = tuple(dataset)[4]
            if tmp_description == "":
                tmp_description = "无"
            tmp["description"] = tmp_description
            datasets.append(tmp.copy())
        logging.info(datasets)

    close_db()

    # 接口约定:
    # status: 状态码
    # total: 总项目数
    # datasets: 数据集数组
    return {
        "status": status,
        "total": total,
        "datasets": datasets
    }

# 获取数据集名称
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
    c.execute("SELECT name FROM dataset WHERE id=?", t)
    res = c.fetchone()
    name = tuple(res)[0]
    status = 1
    close_db()

    # 接口约定:
    return {
        "status": status,
        "name": name
    }

# 获取数据集数据
@bp.route('get-data/', methods = ['POST'])
def getData():
    # 变量初始化 & 接收请求数据
    status = 0
    total = 0
    data = []
    columns = []
    received_data = request.get_json(silent=True)

    # logging
    logging.info("received_data: " + json.dumps(received_data))

    # 应该接收到有:
    # id, num, start[not index]
    dataset_id = received_data['id']
    num = received_data['num']
    start = received_data['start']

    db = get_db()
    c = db.cursor()

    # 通过 dataset_id 获取 project_id 和 filename
    t = (dataset_id,)
    c.execute("SELECT project_id, filename FROM dataset WHERE id=?", t)
    res = c.fetchone()
    project_id = tuple(res)[0]
    filename = tuple(res)[1]

    # 通过 project_id 获取 username
    t = (project_id,)
    c.execute("SELECT username FROM project WHERE id=?", t)
    res = c.fetchone()
    username = tuple(res)[0]

    # 拼接出 hdfs_path，获得数据集 df
    hdfs_path = "/user/" + username + "/" + str(project_id) + "/" + filename + ".parquet"
    df = get_spark().read.load(hdfs_path)

    # 获取 total
    total = df.count()

    # 获取 columns
    tmp = {
        "title": "",
        "dataIndex": "",
    }
    tmp["title"] = "id"
    tmp["dataIndex"] = "id"
    columns.append(tmp.copy())
    for column in df.columns:
        tmp["title"] = column
        tmp["dataIndex"] = column
        columns.append(tmp.copy())

    # 获取 data
    tmp = {}
    key = 0
    for row in df.collect()[start - 1: start + num - 1]:
        tmp["id"] = str(start + key)
        key = key + 1
        tmp["key"] = str(key)
        for column in df.columns:
            tmp[column] = row[column]
        data.append(tmp.copy())

    status = 1

    # 接口约定:
    # status: 状态码
    # total: 数据项数
    # columns: 列名
    # data: 数据
    return {
        "status": status,
        "total": total,
        "columns": columns,
        "data": data
    }
