DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS dataset;
DROP TABLE IF EXISTS model;
DROP TABLE IF EXISTS algorithm;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  permission INTEGER NOT NULL
);

CREATE TABLE project (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT
);

CREATE TABLE dataset (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  project_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  filename TEXT NOT NULL,
  description TEXT
);

CREATE TABLE model (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  project_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  type INTEGER NOT NULL,
  dataset_id INTEGER NOT NULL,
  label_index INTEGER NOT NULL
);

CREATE TABLE algorithm (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  description TEXT
);

INSERT INTO user (username, password, permission) VALUES ('admin', '123', 15);
INSERT INTO user (username, password, permission) VALUES ('Charles', '123', 11);
INSERT INTO user (username, password, permission) VALUES ('Bill', '123', 10);
INSERT INTO user (username, password, permission) VALUES ('Niki', '123', 6);
INSERT INTO user (username, password, permission) VALUES ('Linda', '123', 7);
INSERT INTO user (username, password, permission) VALUES ('Fred', '123', 3);
INSERT INTO user (username, password, permission) VALUES ('Karl', '123', 14);
INSERT INTO user (username, password, permission) VALUES ('Barbara', '123', 12);
INSERT INTO user (username, password, permission) VALUES ('Lee', '123', 1);
INSERT INTO user (username, password, permission) VALUES ('John', '123', 9);
INSERT INTO user (username, password, permission) VALUES ('Doris', '123', 10);
INSERT INTO user (username, password, permission) VALUES ('Tracy', '123', 6);
INSERT INTO user (username, password, permission) VALUES ('Kevin', '123', 14);
INSERT INTO user (username, password, permission) VALUES ('Henry', '123', 11);
INSERT INTO user (username, password, permission) VALUES ('Debbie', '123', 15);
INSERT INTO user (username, password, permission) VALUES ('Scott', '123', 12);
INSERT INTO user (username, password, permission) VALUES ('Kris', '123', 4);
INSERT INTO user (username, password, permission) VALUES ('Peter', '123', 6);

INSERT INTO project (username, name, description) VALUES ('admin', '演示项目1', "多分类问题（txt 文件导入");
INSERT INTO project (username, name, description) VALUES ('admin', '演示项目2', "二分类问题（csv 文件导入");
INSERT INTO project (username, name, description) VALUES ('admin', '演示项目3', "大数据集");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目1', "");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目2', "");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目3', "测试用");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目4', "随机森林算法");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目5', "");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目6', "逻辑回归");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目7', "机器学习");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目8', "");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目9', "Hadoop");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目10', "");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目11', "深度学习");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目12', "梯度提升树");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目13', "学习率");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目14', "训练集和测试集");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目15', "");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目16', "朴素贝叶斯");