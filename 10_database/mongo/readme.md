# Mongo DB

## 介绍

MongoDB是用C++开发的，一个是高性能，开源，无模式的文档型数据库。 
在许多场景下，用于替代传统关系型数据库 或 健值对存储方式

### NOSQL
> not only sql 非关系型数据库

NoSQL，指的是非关系型的数据库。NoSQL有时也称作Not Only SQL的缩写，是对不同于传统的关系型数据库的数据库管理系统的统称。

NoSQL用于超大规模数据的存储。（例如谷歌或Facebook每天为他们的用户收集万亿比特的数据）。这些类型的数据存储不需要固定的模式，无需多余操作就可以横向扩展。

1. High performance 高并发读写的需求
2. huge storage 对海量数据的高效率存储和访问的需求
3. high scalability  & High Availability 对数据库的高可扩展型和高可用的需求


#### NoSQL的优点/缺点

优点:

- 高可扩展性
- 分布式计算
- 低成本
- 架构的灵活性，半结构化数据
- 没有复杂的关系

缺点:

- 没有标准化
- 有限的查询功能（到目前为止）
- 最终一致是不直观的程序

### 关系型数据库
优点：
 1. 事务的一致性
 2. 督学实时
 3. 对复杂sql查询，关联查询的需求


关系型数据库遵循ACID规则

事务在英文中是transaction，和现实世界中的交易很类似，它有如下四个特性：

1、A (Atomicity) 原子性

原子性很容易理解，也就是说事务里的所有操作要么全部做完，要么都不做，事务成功的条件是事务里的所有操作都成功，只要有一个操作失败，整个事务就失败，需要回滚。

比如银行转账，从A账户转100元至B账户，分为两个步骤：1）从A账户取100元；2）存入100元至B账户。这两步要么一起完成，要么一起不完成，如果只完成第一步，第二步失败，钱会莫名其妙少了100元。

2、C (Consistency) 一致性

一致性也比较容易理解，也就是说数据库要一直处于一致的状态，事务的运行不会改变数据库原本的一致性约束。

例如现有完整性约束a+b=10，如果一个事务改变了a，那么必须得改变b，使得事务结束后依然满足a+b=10，否则事务失败。

3、I (Isolation) 独立性

所谓的独立性是指并发的事务之间不会互相影响，如果一个事务要访问的数据正在被另外一个事务修改，只要另外一个事务未提交，它所访问的数据就不受未提交事务的影响。

比如现在有个交易是从A账户转100元至B账户，在这个交易还未完成的情况下，如果此时B查询自己的账户，是看不到新增加的100元的。

4、D (Durability) 持久性

持久性是指一旦事务提交后，它所做的修改将会永久的保存在数据库上，即使出现宕机也不会丢失。

### MongoDB

MongoDB 是一个介于关系数据库和
MongoDB 旨在为WEB应用提供可扩展的高性能数据存储解决方案。

MongoDB 将数据存储为一个文档，数据结构由键值(key=>value)对组成。MongoDB 文档类似于 JSON 对象。字段值可以包含其他文档，数组及文档数组。

1. 面向集合 Collection-Oriented

2. 模式自由

3. 文档型

 
## 启动与链接

mongodb 和 sql 概念

database databse
table   collection
row document
column  field


### 基础命令

* show databses;
* use dataName : 使用某个数据库/ 没有则创建
* db.dropDatabase() ： 删除当前数据库
* show tables
* show collections
* db.createCollection(集合名，{capped:true,size:num}) : 创建集合
* db.tableName.drop()   删除集合

### Object ID

* 每个文档都一个属性，为_id，保证每个文档的唯一性
* 可以自己去设置_id插入文档
* 默认，为每个文档提供一个独特的_id，类型为objectID
* objectID是一个12字节的十六进制数
    * 前4个字节是当前时间戳
    * 接下来3个字节的机器码
    * 接下来的2个字节中mongodb的服务进程ID
    * 最后3个字节是简单的增量值
    
 
## python 中的mongo

### 使用pymongo链接mongodb
> [pymongo](https://api.mongodb.com/python/3.4.0/api/pymongo/index.html) Python driver for MongoDB

#### 查找

* find 返回生成器对象
* find_one 返回一条数据

```
  result = movie.find_one()
  result = movie.find_one({'name':'a'})
    



```

