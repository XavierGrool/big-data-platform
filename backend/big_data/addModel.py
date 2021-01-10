from flask import Blueprint, request
from big_data.db import get_db, close_db
import json
from big_data.spark import get_spark, get_client
import urllib.parse

from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import RFormula
from pyspark.ml.feature import StandardScaler

from pyspark.ml.classification import LogisticRegression
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.classification import GBTClassifier
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.classification import LinearSVC
from pyspark.ml.regression import LinearRegression
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.regression import GBTRegressor
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.evaluation import RegressionEvaluator


import logging
LOG_FORMAT = "/********** %(asctime)s - %(levelname)s - %(message)s **********/"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

bp = Blueprint('add-model', __name__, url_prefix='/add-model')


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


# 数据预处理
def dataPreProcess(df, label, features, problem_type):
    # 把 df 中除 label 列的数据类型是字符串的各列先 StringIndexer 一下
    for i, dtype in enumerate(df.dtypes):
        if dtype[1] == "string" and i != int(label):
            df = df.withColumnRenamed(dtype[0], dtype[0] + "_old")
            indexer = StringIndexer(inputCol = dtype[0] + "_old", outputCol = dtype[0])
            df = indexer.fit(df).transform(df)

    # 如果是分类问题，用 StringIndexer 对 label 列进行处理
    if problem_type != 3:
        label_name = df.dtypes[int(label)][0]
        df = df.withColumnRenamed(label_name, label_name + "_old")
        indexer = StringIndexer(inputCol = label_name + "_old", outputCol = label_name)
        df = indexer.fit(df).transform(df)

    # 装配 label 和 features vector
    formula_str = df.columns[-1] + "~"
    for feature in features:
        formula_str = formula_str + df.columns[int(feature)] + "+"
    formula_str = formula_str[:-1]
    formula = RFormula(
        formula = formula_str,
        featuresCol = "features",
        labelCol = "label"
    )
    df = formula.fit(df).transform(df)

    # 特征归一化处理
    df = df.withColumnRenamed("features", "features_old")
    standardscaler = StandardScaler().setInputCol("features_old").setOutputCol("features")
    df = standardscaler.fit(df).transform(df)

    return df


# 根据参数配置分类器
def getClassifier(type, params):
    if type == 1: # Logistic Regression
        lr_aggregation_depth = int(params["lr_aggregation_depth"])
        lr_elastic_net_param = float(params["lr_elastic_net_param"])
        lr_fit_intercept = True if params["lr_fit_intercept"] == "true" else False
        lr_max_iter = int(params["lr_max_iter"])
        lr_reg_param = float(params["lr_reg_param"])
        cf = LogisticRegression(
            aggregationDepth = lr_aggregation_depth,
            elasticNetParam = lr_elastic_net_param,
            fitIntercept = lr_fit_intercept,
            maxIter = lr_max_iter,
            regParam = lr_reg_param
        )
    elif type == 2: # Decision Tree Classifier
        dt_max_depth = int(params["dt_max_depth"])
        dt_impurity = params["dt_impurity"]
        cf = DecisionTreeClassifier(
            maxDepth = dt_max_depth,
            impurity = dt_impurity
        )
    elif type == 3: # Random Forest Classifier
        rf_impurity = params["rf_impurity"]
        rf_max_depth = int(params["rf_max_depth"])
        rf_num_trees = int(params["rf_num_trees"])
        cf = RandomForestClassifier(
            impurity = rf_impurity,
            maxDepth = rf_max_depth,
            numTrees = rf_num_trees
        )
    elif type == 4: # Gradient-boosted Tree Classifier
        gbt_max_depth = int(params["gbt_max_depth"])
        gbt_max_iter = int(params["gbt_max_iter"])
        gbt_step_size = float(params["gbt_step_size"])
        gbt_subsampling_rate = float(params["gbt_subsampling_rate"])
        cf = GBTClassifier(
            maxDepth = gbt_max_depth,
            maxIter = gbt_max_iter,
            stepSize = gbt_step_size,
            subsamplingRate = gbt_subsampling_rate
        )
    elif type == 5: # Naive Bayes
        nb_smoothing = float(params["nb_smoothing"])
        nb_model_type = params["nb_model_type"]
        cf = NaiveBayes(
            smoothing = nb_smoothing,
            modelType = nb_model_type
        )
    elif type == 6: # Linear Support Vector Machine
        lsvc_max_iter = int(params["lsvc_max_iter"])
        lsvc_reg_param = float(params["lsvc_reg_param"])
        lsvc_fit_intercept = True if params["lsvc_fit_intercept"] == "true" else False
        lsvc_standardization = True if params["lsvc_standardization"] == "true" else False
        lsvc_aggregation_depth = int(params["lsvc_aggregation_depth"])
        cf = LinearSVC(
            maxIter = lsvc_max_iter,
            regParam = lsvc_reg_param,
            fitIntercept = lsvc_fit_intercept,
            standardization = lsvc_standardization,
            aggregationDepth = lsvc_aggregation_depth
        )
    elif type == 7: # Linear Regression
        l_rgs_max_iter = int(params["l_rgs_max_iter"])
        l_rgs_reg_param = float(params["l_rgs_reg_param"])
        cf = LinearRegression(
            maxIter = l_rgs_max_iter,
            regParam = l_rgs_reg_param,
        )
    elif type == 8: # Random Forest Regression
        rf_rgs_max_depth = int(params["rf_rgs_max_depth"])
        rf_rgs_num_trees = int(params["rf_rgs_num_trees"])
        cf = RandomForestRegressor(
            maxDepth = rf_rgs_max_depth,
            numTrees = rf_rgs_num_trees
        )
    elif type == 9: # Gradient-boosted Tree Regression
        gbt_rgs_max_depth = int(params["gbt_rgs_max_depth"])
        gbt_rgs_max_iter = int(params["gbt_rgs_max_iter"])
        cf = GBTRegressor(
            maxDepth = gbt_rgs_max_depth,
            maxIter = gbt_rgs_max_iter
        )

    return cf


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


# 训练模型
@bp.route('train/', methods = ['POST'])
def train():
    # 变量初始化 & 接收请求数据
    status = 0
    results = {}
    received_data = request.get_json(silent=True)

    # logging
    logging.info("received_data: " + json.dumps(received_data))

    # 应该接收到有:
    # dataset_id, label, features, problem_type, classifier, classifier_params
    dataset_id = received_data['dataset_id']
    label = received_data['label']
    features = received_data['features']
    problem_type = received_data['problem_type']
    classifier = received_data['classifier']
    classifier_params = received_data['classifier_params']

    # 获取 dataframe
    df = getDF(dataset_id)

    # 数据预处理
    df = dataPreProcess(df, label, features, problem_type)

    # 划分训练集和测试集
    (trainingData, testData) = df.randomSplit([0.7, 0.3])

    # 训练
    cf = getClassifier(classifier, classifier_params)
    model = cf.fit(trainingData)

    # 把训练好的模型分别作用在训练集和测试集上
    predict_train = model.transform(trainingData)
    predict_test = model.transform(testData)

    # 模型评估
    if problem_type == 1: # 二分类问题
        evaluator = BinaryClassificationEvaluator( # 计算 area under ROC
            rawPredictionCol = "rawPrediction",
            labelCol = "label"
        )
        results["train_roc"] = evaluator.evaluate(predict_train)
        results["test_roc"] = evaluator.evaluate(predict_test)

        evaluator = BinaryClassificationEvaluator( # 计算 area under PR
            rawPredictionCol = "rawPrediction",
            labelCol = "label", 
            metricName = "areaUnderPR"
        )
        results["train_pr"] = evaluator.evaluate(predict_train)
        results["test_pr"] = evaluator.evaluate(predict_test)

    elif problem_type == 2: # 多分类问题
        evaluator = MulticlassClassificationEvaluator( # 计算 acc
            labelCol = "label",
            predictionCol = "prediction",
            metricName = 'accuracy'
        )
        results["train_acc"] = evaluator.evaluate(predict_train)
        results["test_acc"] = evaluator.evaluate(predict_test)

        evaluator = MulticlassClassificationEvaluator( # 计算 f1 score
            labelCol = "label",
            predictionCol = "prediction",
            metricName = 'f1'
        )
        results["train_f1"] = evaluator.evaluate(predict_train)
        results["test_f1"] = evaluator.evaluate(predict_test)
    elif problem_type == 3: # 回归问题
        evaluator = RegressionEvaluator( # 计算 rmse
            labelCol = "label",
            predictionCol = "prediction",
            metricName = 'rmse'
        )
        results["train_rmse"] = evaluator.evaluate(predict_train)
        results["test_rmse"] = evaluator.evaluate(predict_test)

        evaluator = RegressionEvaluator( # 计算 mae
            labelCol = "label",
            predictionCol = "prediction",
            metricName = 'mae'
        )
        results["train_mae"] = evaluator.evaluate(predict_train)
        results["test_mae"] = evaluator.evaluate(predict_test)

    status = 1

    # 接口约定：
    # status: 状态码
    # results: 评估结果
    return {
        "status": status,
        "results": results
    }


# 保存模型
@bp.route('save/', methods = ['POST'])
def save():
    # 变量初始化 & 接收请求数据
    status = 0
    received_data = request.get_json(silent=True)

    # logging
    logging.info("received_data: " + json.dumps(received_data))

    # 应该接收到有:
    # dataset_id, label, features, problem_type, classifier
    # classifier_params, model_name, model_description
    dataset_id = received_data['dataset_id']
    label = received_data['label']
    features = received_data['features']
    problem_type = received_data['problem_type']
    classifier = received_data['classifier']
    classifier_params = received_data['classifier_params']
    model_name = received_data['model_name']
    model_description = received_data['model_description']

    # 获取 dataframe
    df = getDF(dataset_id)

    # 数据预处理
    df = dataPreProcess(df, label, features, problem_type)

    # 训练
    cf = getClassifier(classifier, classifier_params)
    model = cf.fit(df)

    db = get_db()
    c = db.cursor()

    #####################
    # 在 hdfs 中保存模型 #
    #####################

    # 通过 dataset_id 获取 project_id
    t = (dataset_id,)
    c.execute("SELECT project_id FROM dataset WHERE id=?", t)
    res = c.fetchone()
    project_id = tuple(res)[0]

    # 通过 project_id 获取 username
    t = (project_id,)
    c.execute("SELECT username FROM project WHERE id=?", t)
    res = c.fetchone()
    username = tuple(res)[0]

    # 拼接出 model_path 并保存模型
    model_path = "/user/" + username + "/" + str(project_id) + "/" + urllib.parse.quote(model_name)
    model.save(model_path)

    ####################
    # 在数据库中进行记录 #
    ####################

    t = (project_id, model_name, model_description, classifier, dataset_id, int(label))
    c.execute("INSERT INTO model (project_id, name, description, type, dataset_id, label_index) VALUES (?, ?, ?, ?, ?, ?)", t)
    db.commit()
    close_db()

    status = 1

    # 接口约定：
    # status: 状态码
    return {
        "status": status
    }
