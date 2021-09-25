# Hive
> Hive 是基于Hadoop的数据仓库

数据仓库： 

## 数据仓库
> 数据仓库是： 面向主题的，集成的，不可更新的，随时间不变化的数据集合。（用于支持企业或组织的决策分析处理）
数据仓库就是做查询操作的

数据源 -》 数据存储/处理 -》 数据仓库引擎 》 前端展示


OLTP:
面向对象，（银行）

OLAP
联机分析系统 （商品推荐/查询）

数据模型： 1 星形模型  2 雪花模型


## Hive数据仓库

* Hive是建立在 Hadoop HDFS上的数据仓库基础架构
* Hive可以进行数据提取转化加载（ETL）
* Hive定义了简单的类似SQL查询语言。HQL 
* MapReduce开发自定义的mapper和reducer来处理内建的mapper和reducer无法完成的复制的分析工作
* Hive是SQL解析引擎，将SQL语句转移成M/R Job 然后在Hadoop执行
* Hive的表就是 HDFS上的目录/文件

### 元数据

* hive 将元数据存储在数据库中（metastore） 支持mysql， derby等
* hive 中元数据包含表的名字，表的列和分区及其属性，表的属性，表的数据所在目录等


### Hive查询语法

* 解释器，编译器，优化器 完成HQL查询语句 从词法分析、语法分析、编译、优化、及其查询计划的生成
生成的查询计划存储在hDFS中，并随后有MapReduce调用执行

HQL的解析和执行过程

HQL Select -> 解析器（语法分析） -> 编译器（生成hql执行计划） -> 优化器（最佳执行计划） -> 执行

### Hive的体系结构

### hive 的安装

1. 先安装 hadoop
2. 再安装hive

* 嵌入模式安装
    * 元数据被存储在hive自带的derby数据库中
    * 只允许创建一个链接
    * 多用于demo

本地安装模式：
* 元数据信息被存储在mysql数据库中
* mysql数据库和hive在一台服务器上
    
远程模式：
 * msyql和hive不在一个服务器上
 
    







