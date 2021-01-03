from pyspark.sql import SparkSession
from hdfs.client import Client

APP_NAME = "Big Data Platform"

def get_spark():
    spark = SparkSession.builder.appName(APP_NAME).getOrCreate()
    return spark

def get_client():
    return Client("http://namenode:9870/")