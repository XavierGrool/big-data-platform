from flask import Blueprint, request
from big_data.db import get_db, close_db
import json
from big_data.spark import get_spark, get_client
import urllib.parse

from pyspark.ml.feature import IndexToString, StringIndexer
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StandardScaler

from pyspark.ml.classification import LogisticRegressionModel
from pyspark.ml.classification import DecisionTreeClassificationModel
from pyspark.ml.classification import RandomForestClassificationModel
from pyspark.ml.classification import GBTClassificationModel
from pyspark.ml.classification import NaiveBayesModel
from pyspark.ml.classification import LinearSVCModel
from pyspark.ml.regression import LinearRegressionModel
from pyspark.ml.regression import RandomForestRegressionModel
from pyspark.ml.regression import GBTRegressionModel


import logging
LOG_FORMAT = "/********** %(asctime)s - %(levelname)s - %(message)s **********/"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

bp = Blueprint('prediction', __name__, url_prefix='/prediction')


# 根据 dataset_id 获取 dataframe
def getDF(dataset_id):
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

    return df


# 特征装配
def featuresAssemble(df, features):
    # 把 df 中数据类型是字符串的各列先 StringIndexer 一下
    for i, dtype in enumerate(df.dtypes):
        if dtype[1] == "string":
            df = df.withColumnRenamed(dtype[0], dtype[0] + "_old")
            indexer = StringIndexer(inputCol = dtype[0] + "_old", outputCol = dtype[0])
            df = indexer.fit(df).transform(df)

    # 装配特征
    # input_cols = []
    # for feature in features:
    #     input_cols.append(feature)
    assembler = VectorAssembler(inputCols = features, outputCol = "features")
    df = assembler.transform(df)

    # 特征归一化处理
    df = df.withColumnRenamed("features", "features_old")
    standardscaler = StandardScaler().setInputCol("features_old").setOutputCol("features")
    df = standardscaler.fit(df).transform(df)

    return df


# 获取当前项目下的数据集
@bp.route('get-dataset/', methods = ['POST'])
def getDataset():
    # 变量初始化 & 接收请求数据
    status = 0
    dataset_num = 0
    datasets = []
    received_data = request.get_json(silent=True)

    # logging
    logging.info("received_data: " + json.dumps(received_data))

    # 应该接收到有:
    # project_id
    project_id = received_data['id']

    # 获取数据集数量
    db = get_db()
    c = db.cursor()
    t = (project_id,)
    c.execute("SELECT COUNT(*) from dataset WHERE project_id=?", t)
    res = c.fetchone()
    dataset_num = tuple(res)[0]

    # 获取数据集
    if dataset_num == 0:
        datasets = []
    else:
        tmp = {
            "id": 0,
            "name": ""
        }
        for dataset in c.execute("SELECT id, name FROM dataset WHERE project_id=?", t):
            tmp["id"] = tuple(dataset)[0]
            tmp["name"] = tuple(dataset)[1]
            datasets.append(tmp.copy())

    status = 1

    # 接口约定：
    # status: 状态码
    # dataset_num: 数据集数量
    # datasets: 数据集数组
    #     [{"id": "...", "name": "..."}]
    return {
        "status": status,
        "dataset_num": dataset_num,
        "datasets": datasets
    }


# 获取当前项目下的模型
@bp.route('get-model/', methods = ['POST'])
def getModel():
    # 变量初始化 & 接收请求数据
    status = 0
    model_num = 0
    models = []
    received_data = request.get_json(silent=True)

    # logging
    logging.info("received_data: " + json.dumps(received_data))

    # 应该接收到有:
    # project_id
    project_id = received_data['id']

    # 获取模型数量
    db = get_db()
    c = db.cursor()
    t = (project_id,)
    c.execute("SELECT COUNT(*) from model WHERE project_id=?", t)
    res = c.fetchone()
    model_num = tuple(res)[0]

    # 获取模型
    if model_num == 0:
        models = []
    else:
        tmp = {
            "id": 0,
            "name": ""
        }
        for model in c.execute("SELECT id, name FROM model WHERE project_id=?", t):
            tmp["id"] = tuple(model)[0]
            tmp["name"] = tuple(model)[1]
            models.append(tmp.copy())

    status = 1

    # 接口约定：
    # status: 状态码
    # model_num: 模型数量
    # models: 模型数组
    #     [{"id": "...", "name": "..."}]
    return {
        "status": status,
        "model_num": model_num,
        "models": models
    }


# 获取数据集的列
@bp.route('get-columns/', methods = ['POST'])
def getColumns():
    # 变量初始化 & 接收请求数据
    status = 0
    columns = []
    received_data = request.get_json(silent=True)

    # logging
    logging.info("received_data: " + json.dumps(received_data))

    # 应该接收到有:
    # dataset_id
    dataset_id = received_data['dataset_id']

    # 获取 dataframe
    df = getDF(dataset_id)

    # 获取 columns
    tmp = {
        "index": 0,
        "name": "",
    }
    for i, column in enumerate(df.columns):
        tmp["index"] = i
        tmp["name"] = column
        columns.append(tmp.copy())

    status = 1

    # 接口约定：
    # status: 状态码
    # columns: 列
    return {
        "status": status,
        "columns": columns
    }


# 预测
@bp.route('predict/', methods = ['POST'])
def predict():
    # 变量初始化 & 接收请求数据
    status = 0
    columns = []
    predictions = []
    received_data = request.get_json(silent=True)

    # logging
    logging.info("received_data: " + json.dumps(received_data))

    # 应该接收到有:
    # model_id, dataset_id, features
    model_id = received_data['model_id']
    dataset_id = received_data['dataset_id']
    feature_indexers = received_data['features']

    # 获取 dataframe
    df = getDF(dataset_id)

    # 把特征索引转换为特征名称
    features = []
    for feature in feature_indexers:
        features.append(df.columns[int(feature)])

    # 特征装配
    df = featuresAssemble(df, features)

    db = get_db()
    c = db.cursor()

    ################################
    # 根据 model_id 获取 model_path #
    ################################

    # 通过 model_id 获取 project_id, model_name,
    # classifier_type, train_dataset, label_index
    t = (model_id,)
    c.execute("SELECT * FROM model WHERE id=?", t)
    res = c.fetchone()
    project_id = tuple(res)[1]
    model_name = tuple(res)[2]
    classifier_type = tuple(res)[4]
    train_dataset = tuple(res)[5]
    label_index = tuple(res)[6]

    # 通过 project_id 获取 username
    t = (project_id,)
    c.execute("SELECT username FROM project WHERE id=?", t)
    res = c.fetchone()
    username = tuple(res)[0]

    # 拼接 model_path
    model_path = "/user/" + username + "/" + str(project_id) + "/" + urllib.parse.quote(model_name)

    ########
    # 预测 #
    ########

    # 加载模型
    if classifier_type == 1: # Logistic Regression
        model = LogisticRegressionModel.load(model_path)
    elif classifier_type == 2: # Decision Tree Classifier
        model = DecisionTreeClassificationModel.load(model_path)
    elif classifier_type == 3: # Random Forest Classifier
        model = RandomForestClassificationModel.load(model_path)
    elif classifier_type == 4: # Gradient-boosted Tree Classifier
        model = GBTClassificationModel.load(model_path)
    elif classifier_type == 5: # Naive Bayes
        model = NaiveBayesModel.load(model_path)
    elif classifier_type == 6: # Linear Support Vector Machine
        model = LinearSVCModel.load(model_path)
    elif classifier_type == 7: # Linear Regression
        model = LinearRegressionModel.load(model_path)
    elif classifier_type == 8: # Random Forest Regression
        model = RandomForestRegressionModel.load(model_path)
    elif classifier_type == 9: # Gradient-boosted Tree Regression
        model = GBTRegressionModel.load(model_path)

    # 预测
    prediction = model.transform(df)

    ############################################
    # 把分类问题中 index 过的结果还原为原本的样子 #
    ############################################

    classify_type = [1, 2, 3, 4, 5 ,6]
    if classifier_type in classify_type:

        # 获取 train_df
        train_df = getDF(train_dataset)

        # 获取 label 的列名
        label_col_name = train_df.dtypes[label_index][0]

        # 先用 StringIndexer 处理一下 label 列
        train_df = train_df.withColumnRenamed(label_col_name, label_col_name + "_old")
        indexer = StringIndexer(inputCol = label_col_name + "_old", outputCol = label_col_name)
        train_df = indexer.fit(train_df).transform(train_df)

        # 获取 metadata
        label_metadata = train_df.schema[label_col_name].metadata["ml_attr"]["vals"]

        # 把现在 prediction 中的预测结果转换回去
        prediction = prediction.withColumnRenamed("prediction", "prediction_old")
        converter = IndexToString(
            inputCol = "prediction_old",
            outputCol = "prediction"
        ).setLabels(label_metadata)
        prediction = converter.transform(prediction)

    ###################
    # 整理要返回的数据 #
    ###################

    # 获取 columns
    tmp = {
        "title": "",
        "dataIndex": "",
    }
    tmp["title"] = "id"
    tmp["dataIndex"] = "id"
    columns.append(tmp.copy())
    for column in features:
        tmp["title"] = column
        tmp["dataIndex"] = column
        columns.append(tmp.copy())
    tmp["title"] = "prediction"
    tmp["dataIndex"] = "prediction"
    columns.append(tmp.copy())

    # 获取 predictions
    tmp = {}
    id = 1
    for row in prediction.collect():
        tmp["id"] = str(id)
        tmp["key"] = str(id)
        id = id + 1
        for column in features:
            tmp[column] = row[column]
        tmp["prediction"] = row["prediction"]
        predictions.append(tmp.copy())

    status = 1

    # 接口约定：
    # status: 状态码
    # columns: 列名
    # predictions: 预测结果
    return {
        "status": status,
        "columns": columns,
        "predictions": predictions
    }
