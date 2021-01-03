DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS dataset;
DROP TABLE IF EXISTS model;

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
  description TEXT
);

INSERT INTO user (username, password, permission) VALUES ('admin', '123456', 16);
INSERT INTO user (username, password, permission) VALUES ('Charles', '123', 15);
INSERT INTO user (username, password, permission) VALUES ('Bill', '123', 15);
INSERT INTO user (username, password, permission) VALUES ('Niki', '123', 15);
INSERT INTO user (username, password, permission) VALUES ('Linda', '123', 15);
INSERT INTO user (username, password, permission) VALUES ('Fred', '123', 15);
INSERT INTO user (username, password, permission) VALUES ('Karl', '123', 15);
INSERT INTO user (username, password, permission) VALUES ('Barbara', '123', 15);
INSERT INTO user (username, password, permission) VALUES ('Lee', '123', 15);
INSERT INTO user (username, password, permission) VALUES ('John', '123', 15);
INSERT INTO user (username, password, permission) VALUES ('Doris', '123', 15);
INSERT INTO user (username, password, permission) VALUES ('Tracy', '123', 15);
INSERT INTO user (username, password, permission) VALUES ('Kevin', '123', 15);
INSERT INTO user (username, password, permission) VALUES ('Henry', '123', 15);
INSERT INTO user (username, password, permission) VALUES ('Debbie', '123', 15);
INSERT INTO user (username, password, permission) VALUES ('Scott', '123', 15);
INSERT INTO user (username, password, permission) VALUES ('Kris', '123', 15);
INSERT INTO user (username, password, permission) VALUES ('Peter', '123', 15);

INSERT INTO project (username, name, description) VALUES ('admin', '我的项目1', "");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目2', "");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目3', "hhhhh");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目4', "啦啦啦啦了");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目5', "");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目6', "哈哈哈哈哈哈哈哈哈哈");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目7', "1234567");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目8', "~~~");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目9', "big-data");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目10', "");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目11', "i love Hadoop");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目12', "");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目13', "");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目14', "test");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目15', "!");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目16', "Hello world!~");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目17', "meat");
INSERT INTO project (username, name, description) VALUES ('admin', '我的项目18', "soul");