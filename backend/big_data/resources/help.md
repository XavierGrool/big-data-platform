# 大数据分析工具平台使用手册

## 1. 系统部署
### 1.1 项目运行环境
docker

为方便阐述，下文默认是在 win10 下运行 docker 客户端

### 1.2 概述
本项目的 docker-compose 基本框架来源于 https://github.com/big-data-europe/docker-hadoop ，受 pr59 启发最终得到了现有版本。另外还有一些因项目需要而进行的更改。

### 1.3 部署方式
把项目拉取到本地后，请务必保证项目路径没有中文字符，并修改 `namenode` 服务及 `my-spark` 服务中 `volumes` 的地址。为了方便起见，这里我在项目根目录建立了一个 `share` 文件夹用于容器与 win10 的共享文件夹。第一次启动前，首先启动一次 Hadoop 集群，把 `/etc/hadoop` 中的所有配置文件复制出来到 `share` 文件夹里（比如 /share/hadoop），之后的每次就可以在 `my-spark` 服务中把 `/share/hadoop` 挂载到 `/etc/hadoop` 中，以确保 `pyspark` 能连接到 yarn 集群。

### 1.4 启动命令
```
docker-compose up -d
```

### 1.5 关闭命令
```
docker-compose down --remove-orphans
docker volume rm big-data-platform_hadoop_datanode1 big-data-platform_hadoop_datanode2 big-data-platform_hadoop_datanode3 big-data-platform_hadoop_historyserver big-data-platform_hadoop_namenode
```


## 2. 系统登陆
### 2.1 网址
[http://localhost:8080](http://localhost:8080)

### 2.2 推荐浏览器
推荐使用
- Microsoft Edge
- Chrome
- Firefox

### 2.3 网络环境
处于同一局域网下可以使用局域网内 ip 地址进行访问，在局域网外环境需要端口转发

### 2.4 账号与密码
默认管理员账户：admin

默认管理员密码：123456

![登录界面](http://futureyu.cn:8000/pics/1.png)

## 3. 用户管理
在用户管理界面可以添加、修改或删除用户。

![用户管理界面](http://futureyu.cn:8000/pics/2.png)

添加用户需要输入用户名、密码、权限。

![用户管理界面-添加](http://futureyu.cn:8000/pics/3.png)

修改用户需要输入新权限，用户名不可修改。

![用户管理界面-修改](http://futureyu.cn:8000/pics/4.png)


删除用户时需要二次确认。

![用户管理界面-删除](http://futureyu.cn:8000/pics/5.png)

![用户管理界面-删除](http://futureyu.cn:8000/pics/6.png)

## 4. 项目空间
项目流程图如下所示：

![项目流程图](http://futureyu.cn:8000/pics/0.png)

### 4.1 项目管理
项目空间中支持新增、删除、修改功能

![项目管理界面](http://futureyu.cn:8000/pics/7.png)

添加项目需要输入项目名称、描述（可选）。

![项目管理界面-添加](http://futureyu.cn:8000/pics/8.png)

修改项目详情可以修改项目名称与描述。

![项目管理界面-修改](http://futureyu.cn:8000/pics/9.png)

删除项目时需要二次确认。

![项目管理界面-删除](http://futureyu.cn:8000/pics/10.png)

![项目管理界面-删除](http://futureyu.cn:8000/pics/11.png)

### 4.2 数据集
点击项目名称可以进入该项目的具体数据管理，左侧栏分为数据集、模型管理、预测分析。

在此界面可以对数据集进行变更与删除操作。

![数据集界面](http://futureyu.cn:8000/pics/12.png)

点击添加数据集按钮，可以添加数据集，需要先上传数据集并为其命名，之后需要输入该文件的分隔符以及每一列的命名以及数据类型，之后点击提交即可。

![添加数据集](http://futureyu.cn:8000/pics/13.png)

### 4.2 模型管理
在模型管理界面可以添加、修改、删除模型。

![模型界面](http://futureyu.cn:8000/pics/14.png)

点击添加模型按钮，可以根据数据集添加模型，首先先选择数据集并为其选择 Lable 以及 Feature，之后确定问题分类，系统会自动推荐模型，用户也可以手动修改其中的参数，之后点击开始训练即可。

![添加模型](http://futureyu.cn:8000/pics/15.jpeg)

训练完成后可以看到该模型的准确率，用户可以自主决定是否保存。

![保存模型](http://futureyu.cn:8000/pics/16.png)

### 4.3 预测分析
点击左侧预测分析之后，首先点击选择模型，选取之前保存过的模型，然后选择测试集，并选择 Feature，在点击开始预测之后，系统会根据模型自动对测试集进行预测分析。

![预测分析](http://futureyu.cn:8000/pics/17.jpg)

