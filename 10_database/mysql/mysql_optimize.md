# MySQL 调优

## MySQL开发规范


## SQL规范性检查

### select检查

#### UDF用户自定义函数

SQL语句的select后面使用了自定义函数UDF，SQL返回多少行，那么UDF函数就会被调用多少次，这是非常影响性能的。

```mysql
# --- getOrderNo是用户自定义一个函数用户来根据order_sn来获取订单编号
select id, payment_id, order_sn, getOrderNo(order_sn) from payment_transaction where status = 1 and create_time between '2020-10-01 10:00:00' and '2020-10-02 10:00:00';
```
#### text类型检查

如果select出现text类型的字段，就会消耗大量的网络和IO带宽，由于返回的内容过大超过max_allowed_packet设置会导致程序报错，需要评估谨慎使用。
```mysql
# 表request_log的中content是text类型。
select user_id, content, status, url, type from request_log where user_id = 32121;
```

#### group_concat谨慎使用

gorup_concat是一个字符串聚合函数，会影响SQL的响应时间，如果返回的值过大超过了max_allowed_packet设置会导致程序报错。
```mysql
select batch_id, group_concat(name) from buffer_batch where status = 0 and create_time between '2020-10-01 10:00:00' and '2020-10-02 10:00:00';
```

#### 内联子查询

在select后面有子查询的情况称为内联子查询，SQL返回多少行，子查询就需要执行过多少次，严重影响SQL性能。
```mysql
select id,(select rule_name from member_rule limit 1) as rule_name, 
       member_id, member_type, member_name, status from member_info m 
       where status = 1 and create_time between '2020-09-02 10:00:00' and '2020-10-01 10:00:00';
```
### from检查

#### 表的链接方式

在MySQL中不建议使用Left Join，即使ON过滤条件列索引，一些情况也不会走索引，导致大量的数据行被扫描，SQL性能变得很差，同时要清楚ON和Where的区别。
```mysql
SELECT a.member_id,a.create_time,b.active_time FROM operation_log a 
       LEFT JOIN member_info b ON a.member_id = b.member_id 
       where  b.`status` = 1 and a.create_time between '2020-10-01 00:00:00' and '2020-10-30 00:00:00' limit 100, 0;
```

#### 子查询

由于MySQL的基于成本的优化器CBO对子查询的处理能力比较弱，不建议使用子查询，可以改写成Inner Join。
```mysql
select b.member_id,b.member_type, a.create_time,a.device_model from member_operation_log a 
       inner join (select member_id,member_type from member_base_info where `status` = 1 and create_time between '2020-10-01 00:00:00' and '2020-10-30 00:00:00') as b 
       on a.member_id = b.member_id;
```

### where检查

#### 索引列被运算

当一个字段被索引，同时出现where条件后面，是不能进行任何运算，会导致索引失效。

```mysql
# device_no列上有索引，由于使用了ltrim函数导致索引失效
select id, name , phone, address, device_no from users where ltrim(device_no) = 'Hfs1212121';
# balance列有索引,由于做了运算导致索引失效
select account_no, balance from accounts where balance + 100 = 10000 and status = 1;
```

####类型转换

对于Int类型的字段，传varchar类型的值是可以走索引，MySQL内部自动做了隐式类型转换；
相反对于varchar类型字段传入Int值是无法走索引的，应该做到对应的字段类型传对应的值总是对的。
```mysql
# user_id是bigint类型，传入varchar值发生了隐式类型转换，可以走索引。
select id, name , phone, address, device_no from users where user_id = '23126';
# card_no是varchar(20)，传入int值是无法走索引
select id, name , phone, address, device_no from users where card_no = 2312612121;
```

#### 列字符集

从MySQL 5.6开始建议所有对象字符集应该使用用utf8mb4，包括MySQL实例字符集，数据库字符集，表字符集，列字符集。

避免在关联查询Join时字段字符集不匹配导致索引失效，同时目前只有utf8mb4支持emoji表情存储。
```mysql
character_set_server  =  utf8mb4    #数据库实例字符集
character_set_connection = utf8mb4  #连接字符集
character_set_database = utf8mb4    #数据库字符集
character_set_results = utf8mb4     #结果集字符集
```

### group by检查

#### 前缀索引

group by后面的列有索引，索引可以消除排序带来的CPU开销，如果是前缀索引，是不能消除排序的。
```mysql
# device_no字段类型varchar(200)，创建了前缀索引。
alter table users add index idx_device_no(device_no(64));
select device_no, count(*) from users 
     where create_time between '2020-10-01 00:00:00' and '2020-10-30 00:00:00' 
     group by device_no;
```

#### 函数运算

假设需要统计某月每天的新增用户量
虽然可以走create_time的索引，但是不能消除排序，可以考虑冗余一个字段stats_date date类型来解决这种问题。
```mysql
select DATE_FORMAT(create_time, '%Y-%m-%d'), count(*) from users 
  where create_time between '2020-09-01 00:00:00' and '2020-09-30 23:59:59' 
  group by DATE_FORMAT(create_time, '%Y-%m-%d');
```

### order by检查
#### 前缀索引

order by后面的列有索引，索引可以消除排序带来的CPU开销，如果是前缀索引，是不能消除排序的。

#### 字段顺序

排序字段顺序，asc/desc升降要跟索引保持一致，充分利用索引的有序性来消除排序带来的CPU开销。

### limit检查

limit m,n要慎重

对于limit m, n分页查询，越往后面翻页即m越大的情况下SQL的耗时会越来越长，对于这种应该先取出主键id，然后通过主键id跟原表进行Join关联查询。

### 表结构检查
#### 表&列名关键字
在数据库设计建模阶段，对表名及字段名设置要合理，不能使用MySQL的关键字，如desc, order, status, group等。同时建议设置lower_case_table_names = 1表名不区分大小写。

#### 表存储引擎
对于OLTP业务系统，建议使用InnoDB引擎获取更好的性能，可以通过参数 default_storage_engine 控制。

#### AUTO_INCREMENT属性
建表的时候主键id带有AUTO_INCREMENT属性，而且AUTO_INCREMENT=1，
在InnoDB内部是通过一个系统全局变量dict_sys.row_id来计数，
row_id是一个8字节的bigint unsigned，
InnoDB在设计时只给row_id保留了6个字节的长度，这样row_id取值范围就是0到2^48 - 1，
如果id的值达到了最大值，下一个值就从0开始继续循环递增，在代码中禁止指定主键id值插入。
```mysql
# 新插入的id值会从10001开始，这是不对的，应该从1开始。
create table booking( `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键id',......) engine = InnoDB auto_increment = 10000;

#指定了id值插入，后续自增就会从该值开始+1，索引禁止指定id值插入。
insert into booking(id, book_sn) values(1234551121, 'N12121');
```

#### NOT NULL属性
根据业务含义，尽量将字段都添加上NOT NULL DEFAULT VALUE属性，如果列值存储了大量的NULL，会影响索引的稳定性。

#### DEFAULT属性
在创建表的时候，建议每个字段尽量都有默认值，禁止DEFAULT NULL，而是对字段类型填充响应的默认值。

#### COMMENT属性
字段的备注要能明确该字段的作用，尤其是某些表示状态的字段，要显式的写出该字段所有可能的状态数值以及该数值的含义。

#### TEXT类型
不建议使用Text数据类型，一方面由于传输大量的数据包可能会超过max_allowed_packet设置导致程序报错，
另一方面表上的DML操作都会变的很慢，建议采用es或者对象存储OSS来存储和检索。

### 索引检查
#### 索引属性
索引基数指的是被索引的列唯一值的个数，唯一值越多接近表的count(*)说明索引的选择率越高，通过索引扫描的行数就越少，性能就越高，

例如主键id的选择率是100%，在MySQL中尽量所有的update都使用主键id去更新，因为id是聚集索引存储着整行数据，不需要回表，性能是最高的。
```mysql
 select count(*) from member_info; # 1 row in set (0.35 sec)
 show index from member_base_info;
```

 * Table： 表名
 * Non_unique ：是否为unique index，0-是，1-否。
 * Key_name：索引名称
 * Seq_in_index：索引中的顺序号，单列索引-都是1；复合索引-根据索引列的顺序从1开始递增。
 * Column_name：索引的列名
 * Collation：排序顺序，如果没有指定asc/desc，默认都是升序ASC。
 * Cardinality：索引基数-索引列唯一值的个数。
 * sub_part：前缀索引的长度；例如index (member_name(10)，长度就是10。
 * Packed：索引的组织方式，默认是NULL。
 * Null：YES:索引列包含Null值；'':索引不包含Null值。
 * Index_type：默认是BTREE，其他的值FULLTEXT，HASH，RTREE。
 * Comment：在索引列中没有被描述的信息，例如索引被禁用。
 * Index_comment：创建索引时的备注。
 
#### 前缀索引
对于变长字符串类型varchar(m)，为了减少key_len，可以考虑创建前缀索引，但是前缀索引不能消除group by， order by带来排序开销。如果字段的实际最大值比m小很多，建议缩小字段长度。
```mysql
alter table member_info add index idx_member_name_part(member_name(10));
```
#### 复合索引顺序

有很多人喜欢在创建复合索引的时候，总以为前导列一定是唯一值多的列，
例如索引index idx_create_time_status(create_time, status)，这个索引往往是无法命中，因为扫描的IO次数太多，总体的cost的比全表扫描还大，CBO最终的选择是走full table scan。

MySQL遵循的是索引最左匹配原则，对于复合索引，从左到右依次扫描索引列，到遇到第一个范围查询（>=, >,<, <=, between ….. and ….）就停止扫描，索引正确的索引顺序应该是 index idx_status_create_time(status, create_time)。
```mysql
select account_no, balance from accounts 
where status = 1 and create_time between '2020-09-01 00:00:00' and '2020-09-30 23:59:59';
```

#### 时间列索引

对于默认字段created_at(create_time)、updated_at(update_time)这种默认就应该创建索引，这一般来说是默认的规则。

## SQL优化案例
通过对慢查询的监控告警，经常发现一些SQL语句where过滤字段都有索引，但是由于SQL写法的问题导致索引失效

[大厂都是怎么SQL调优的？](https://segmentfault.com/a/1190000038177522)
