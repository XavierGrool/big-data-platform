# big-data-platform

项目运行环境：docker

为方便阐述，下文默认是在 win10 下运行 docker 客户端

本项目的 docker-compose 基本框架来源于 https://github.com/big-data-europe/docker-hadoop ，受 pr59 启发最终得到了现有版本。另外还有一些因项目需要而进行的更改。

把项目拉取到本地后，请务必保证项目路径没有中文字符，并修改 `namenode` 服务及 `my-spark` 服务中 `volumes` 的地址。为了方便起见，这里我在项目根目录建立了一个 `share` 文件夹用于容器与 win10 的共享文件夹。第一次启动前，首先启动一次 Hadoop 集群，把 `/etc/hadoop` 中的所有配置文件复制出来到 `share` 文件夹里（比如 /share/hadoop），之后的每次就可以在 `my-spark` 服务中把 `/share/hadoop` 挂载到 `/etc/hadoop` 中，以确保 `pyspark` 能连接到 yarn 集群。

启动命令：
```
docker-compose up -d
```
关闭命令：
```
docker-compose down --remove-orphans
docker volume rm big-data-platform_hadoop_datanode1 big-data-platform_hadoop_datanode2 big-data-platform_hadoop_datanode3 big-data-platform_hadoop_historyserver big-data-platform_hadoop_namenode
```