## Mysql 索引

### 什么是索引
> 索引是数据表中一个或者多个列进行排序的数据结构

索引能够大幅提升检索速度。创建、更新索引本身也会耗费空间和时间

查找结构进化史
1. 线性查找：一个个找；实现简单；太慢
2. 二分查找：有序；简单；要求是有序的，插入特别慢
3. HASH查找：查询快；占用空间；不太适合存储大规模数据
4. 二叉查找树：插入和查询很快(log(n))；无法存大规模数据，复杂度退化
5. 平衡树：解决 BST 退化问题，树是平衡的；节点非常多的时候，依然树高很高
6. 多路查找树：一个父亲多个孩子节点（度）；节点过多树高不会特别深
7. 多路平衡查找树：B-Tree

关于这些查找结果的演示推荐：[数据结构可视化](https://www.cs.usfca.edu/~galles/visualization/Algorithms.html)

比如二叉查找树退化问题：
```
    5
   /
  4
 /
3
```

可以明显看到，由于我们输入的数字是顺序增长的，二叉查找树变成了单边增长的线性结构，这就是复杂度退化。

平衡树(AVL)则没有这个问题：
```
    5            4
   /            / \
  4      =>    3   5
 /
3
```

### 什么是 B-Tree？
* 多路平衡查找树（每个节点最多 m(m>=2) 个孩子，称为 m 阶或者度）
* 叶节点具有相同的深度
* 节点的数据 key 从左到右是递增的

### B+Tree
* Mysql 实际使用的 B+Tree 作为索引的数据结构
* 只在叶子节点带有指向记录的指针（For what？可以增加树的度）
* 叶子节点通过指针相连（For what？实现范围查询）

### 索引类型
> Mysql目前主要有以下几种索引类型：FULLTEXT，HASH，BTREE，RTREE。

1. FULLTEXT 全文索引
  > 目前只有MyISAM引擎支持。其可以在CREATE TABLE ，ALTER TABLE ，CREATE INDEX 使用，不过目前只有 CHAR、VARCHAR ，TEXT 列上可以创建全文索引。
  > 全文索引并不是和MyISAM一起诞生的，它的出现是为了解决WHERE name LIKE “%word%"这类针对文本的模糊查询效率较低的问题。

2. HASH
  > 由于HASH的唯一（几乎100%的唯一）及类似键值对的形式，很适合作为索引。

HASH索引可以一次定位，不需要像树形索引那样逐层查找,因此具有极高的效率。
但是，这种高效是有条件的，即只在“=”和“in”条件下高效，对于范围查询、排序及组合索引仍然效率不高。

3. BTREE
  > BTREE索引就是一种将索引值按一定的算法，存入一个树形的数据结构中（二叉树），每次查询都是从树的入口root开始，依次遍历node，获取leaf。这是MySQL里默认和最常用的索引类型。

4. RTREE
  > RTREE在MySQL很少使用，仅支持geometry数据类型，支持该类型的存储引擎只有MyISAM、BDb、InnoDb、NDb、Archive几种。

  > 相对于BTREE，RTREE的优势在于范围查找。

### Mysql 索引类型
 * 普通类型（CREATE INDEX) 仅加速查询
 * 唯一索引 加速查询 + 列值唯一（可以有null（CREATE UNIQUE INDEX)
 * 主键索引：加速查询 + 列值唯一（不可以有null）+ 表中只有一个
 * 多列索引 / 联合索引 / 组合索引：多列值组成一个索引，专门用于组合搜索，其效率大于索引合并
 * 主键索引（PRIMARY KEY），一个表只能有一个
 * 全文索引（FULLTEXT INDEX），InnoDB 不支持, 对文本的内容进行分词，进行搜索
> 索引合并，使用多个单列索引组合搜索
  覆盖索引，select的数据列只用从索引中就能够取得，不必读取数据行，换句话说查询列要被所建的索引覆盖

* [覆盖索引](https://www.cnblogs.com/happyflyingpig/p/7662881.html)

### 使用索引的注意事项
1. 索引不会包含有NULL值的列
    > 只要列中包含有NULL值都将不会被包含在索引中，复合索引中只要有一列含有NULL值，那么这一列对于此复合索引就是无效的。
    > 所以我们在数据库设计时不要让字段的默认值为NULL。

2. 使用短索引
    > 对串列进行索引，如果可能应该指定一个前缀长度。例如，如果有一个CHAR(255)的列，如果在前10个或20个字符内，多数值是惟一的，那么就不要对整个列进行索引。短索引不仅可以提高查询速度而且可以节省磁盘空间和I/O操作。

3. 索引列排序
    > MySQL查询只使用一个索引，因此如果where子句中已经使用了索引的话，那么order by中的列是不会使用索引的。因此数据库默认排序可以符合要求的情况下不要使用排序操作；尽量不要包含多个列的排序，如果需要最好给这些列创建复合索引。

4. like语句操作
    > 一般情况下不鼓励使用like操作，如果非使用不可，如何使用也是一个问题。like “%aaa%” 不会使用索引而like “aaa%”可以使用索引。

5.不要在列上进行运算 ` select * from users where YEAR(adddate)<2007 ` 将在每个行上进行运算，这将导致索引失效而进行全表扫描

6.不使用NOT IN和<>操作
 
### 什么时候创建索引
 * 经常用作查询条件的字段
 * 经常用作表连接的字段
 * 经常出现在 order by，group by 之后的字段


### 索引什么时候失效？
> 模糊匹配、类型隐转、最左匹配

* 以 % 开头的 LIKE 语法，模糊搜索
* 出现隐式类型转换（在 Python 这种动态语言查询中需要注意）
* 没有满足最左前缀原则

### 什么是聚集索引和非聚集索引？
> 在聚集索引中，表中行的物理顺序与键值的逻辑（索引）顺序相同。
> 一个表只能包含一个聚集索引. 
> 如果某索引不是聚集索引，则表中行的物理顺序与键值的逻辑顺序不匹配。
> 与非聚集索引相比，聚集索引通常提供更快的数据访问速度。

聚集还是非聚集指的是: B+Tree 叶节点存的是指针还是数据记录
MyISAM 索引和数据分离，使用的是非聚集索引
InnoDB 数据文件就是索引文件，主键索引就是聚集索引

#### 辅助索引
还有一个辅助索引，我们也可以了解下。

辅助索引

在以开发工程师的角度来解释数据库索引的原理和如何优化慢查询。



## MySQL索引原理

索引目的: 在于提高查询效率

索引原理
除了词典，生活中随处可见索引的例子，如火车站的车次表、图书的目录等。它们的原理都是一样的，通过不断的缩小想要获得数据的范围来筛选出最终想要的结果，同时把随机的事件变成顺序的事件，也就是我们总是通过同一种查找方式来锁定数据。

数据库也是一样，但显然要复杂许多，因为不仅面临着等值查询，还有范围查询(>、<、between、in)、模糊查询(like)、并集查询(or)等等。

数据库应该选择怎么样的方式来应对所有的问题呢？我们回想字典的例子，能不能把数据分成段，然后分段查询呢？
最简单的如果1000条数据，1到100分成第一段，101到200分成第二段，201到300分成第三段……这样查第250条数据，只要找第三段就可以了，一下子去除了90%的无效数据。
但如果是1千万的记录呢，分成几段比较好？稍有算法基础的同学会想到搜索树，其平均复杂度是lgN，具有不错的查询性能。
但这里我们忽略了一个关键的问题，复杂度模型是基于每次相同的操作成本来考虑的，数据库实现比较复杂，数据保存在磁盘上，而为了提高性能，每次又可以把部分数据读入内存来计算，
因为我们知道访问磁盘的成本大概是访问内存的十万倍左右，所以简单的搜索树难以满足复杂的应用场景。

## 磁盘IO与预读
前面提到了访问磁盘，那么这里先简单介绍一下磁盘IO和预读，
磁盘读取数据靠的是机械运动，每次读取数据花费的时间可以分为寻道时间、旋转延迟、传输时间三个部分，
寻道时间指的是磁臂移动到指定磁道所需要的时间，主流磁盘一般在5ms以下；
旋转延迟就是我们经常听说的磁盘转速，比如一个磁盘7200转，表示每分钟能转7200次，也就是说1秒钟能转120次，旋转延迟就是1/120/2 = 4.17ms；
传输时间指的是从磁盘读出或将数据写入磁盘的时间，一般在零点几毫秒，相对于前两个时间可以忽略不计。
那么访问一次磁盘的时间，即一次磁盘IO的时间约等于5+4.17 = 9ms左右，听起来还挺不错的，但要知道一台500 -MIPS的机器每秒可以执行5亿条指令，因为指令依靠的是电的性质，换句话说执行一次IO的时间可以执行40万条指令，数据库动辄十万百万乃至千万级数据，每次9毫秒的时间，显然是个灾难。

下图是计算机硬件延迟的对比图，供大家参考：

various-system-software-hardware-latencies 

考虑到磁盘IO是非常高昂的操作，计算机操作系统做了一些优化，当一次IO时，不光把当前磁盘地址的数据，而是把相邻的数据也都读取到内存缓冲区内，因为局部预读性原理告诉我们，

当计算机访问一个地址的数据的时候，与其相邻的数据也会很快被访问到。
每一次IO读取的数据我们称之为一页(page)。
具体一页有多大数据跟操作系统有关，一般为4k或8k，也就是我们读取一页内的数据时候，实际上才发生了一次IO，这个理论对于索引的数据结构设计非常有帮助。

索引的数据结构
前面讲了生活中索引的例子，索引的基本原理，数据库的复杂性，又讲了操作系统的相关知识，目的就是让大家了解，
任何一种数据结构都不是凭空产生的，一定会有它的背景和使用场景
，我们现在总结一下，我们需要这种数据结构能够做些什么
其实很简单，那就是：每次查找数据时把磁盘IO次数控制在一个很小的数量级，
最好是常数数量级。那么我们就想到如果一个高度可控的多路搜索树是否能满足需求呢？就这样，b+树应运而生。

详解b+树


如上图，是一颗b+树，关于b+树的定义可以参见B+树，这里只说一些重点，浅蓝色的块我们称之为一个磁盘块，可以看到每个磁盘块包含几个数据项（深蓝色所示）和指针（黄色所示），如磁盘块1包含数据项17和35，包含指针P1、P2、P3，P1表示小于17的磁盘块，P2表示在17和35之间的磁盘块，P3表示大于35的磁盘块。真实的数据存在于叶子节点即3、5、9、10、13、15、28、29、36、60、75、79、90、99。非叶子节点只不存储真实的数据，只存储指引搜索方向的数据项，如17、35并不真实存在于数据表中。

b+树的查找过程
如图所示，如果要查找数据项29，那么首先会把磁盘块1由磁盘加载到内存，此时发生一次IO，在内存中用二分查找确定29在17和35之间，锁定磁盘块1的P2指针，内存时间因为非常短（相比磁盘的IO）可以忽略不计，通过磁盘块1的P2指针的磁盘地址把磁盘块3由磁盘加载到内存，发生第二次IO，29在26和30之间，锁定磁盘块3的P2指针，通过指针加载磁盘块8到内存，发生第三次IO，同时内存中做二分查找找到29，结束查询，总计三次IO。真实的情况是，3层的b+树可以表示上百万的数据，如果上百万的数据查找只需要三次IO，性能提高将是巨大的，如果没有索引，每个数据项都要发生一次IO，那么总共需要百万次的IO，显然成本非常非常高。

b+树性质
1.通过上面的分析，我们知道IO次数取决于b+数的高度h，假设当前数据表的数据为N，每个磁盘块的数据项的数量是m，则有h=㏒(m+1)N，当数据量N一定的情况下，m越大，h越小；而m = 磁盘块的大小 / 数据项的大小，磁盘块的大小也就是一个数据页的大小，是固定的，如果数据项占的空间越小，数据项的数量越多，树的高度越低。这就是为什么每个数据项，即索引字段要尽量的小，比如int占4字节，要比bigint8字节少一半。这也是为什么b+树要求把真实的数据放到叶子节点而不是内层节点，一旦放到内层节点，磁盘块的数据项会大幅度下降，导致树增高。当数据项等于1时将会退化成线性表。

2.当b+树的数据项是复合的数据结构，比如(name,age,sex)的时候，b+数是按照从左到右的顺序来建立搜索树的，比如当(张三,20,F)这样的数据来检索的时候，b+树会优先比较name来确定下一步的所搜方向，如果name相同再依次比较age和sex，最后得到检索的数据；但当(20,F)这样的没有name的数据来的时候，b+树就不知道下一步该查哪个节点，因为建立搜索树的时候name就是第一个比较因子，必须要先根据name来搜索才能知道下一步去哪里查询。比如当(张三,F)这样的数据来检索时，b+树可以用name来指定搜索方向，但下一个字段age的缺失，所以只能把名字等于张三的数据都找到，然后再匹配性别是F的数据了， 这个是非常重要的性质，即索引的最左匹配特性。


### 创建索引有哪些需要注意的？

* 非空字段 NOT NULL，Mysql 很难对空值作查询优化
* 区分度高，离散度大，作为索引的字段值尽量不要有大量相同值
* 索引的长度不要太长（比较耗费时间）

### 建索引的几大原则

1. 最左前缀匹配原则
    > mysql会一直向右匹配直到遇到范围查询(>、<、between、like)就停止匹配
    > 比如 a = 1 and b = 2 and c > 3 and d = 4 如果建立(a,b,c,d)顺序的索引，d是用不到索引的，如果建立(a,b,d,c)的索引则都可以用到，a,b,d的顺序可以任意调整。

2. =和in可以乱序
    > 比如a = 1 and b = 2 and c = 3 建立(a,b,c)索引可以任意顺序，mysql的查询优化器会帮你优化成索引可以识别的形式。

3. 尽量选择区分度高的列作为索引，区分度的公式是count(distinct col)/count(*)，表示字段不重复的比例，比例越大我们扫描的记录数越少，唯一键的区分度是1
   > 而一些状态、性别字段可能在大数据面前区分度就是0，那可能有人会问，这个比例有什么经验值吗？使用场景不同，这个值也很难确定，
   > 一般需要join的字段我们都要求是0.1以上，即平均1条扫描10条记录。

4. 索引列不能参与计算，保持列“干净”，
   > b+树中存的都是数据表中的字段值，但进行检索时，需要把所有元素都应用函数才能比较
   > 比如 from_unixtime(create_time) = ’2014-05-29’ 就不能使用到索引, 应该写成create_time = unix_timestamp(’2014-05-29’)

5. 尽量的扩展索引，不要新建索引
    > 比如表中已经有a的索引，现在要加(a,b)的索引，那么只需要修改原来的索引即可。

### 一个慢查询引发的思考

```mysql
    select
       count(*) 
    from
       task 
    where
       status=2 
       and operator_id=20839 
       and operate_time>1371169729 
       and operate_time<1371174603 
       and type=2;
```

根据最左匹配原则，上面sql语句的索引应该是 status、operator_id、type、operate_time的联合索引；
   其中status、operator_id、type的顺序可以颠倒
   ，所以我才会说，把这个表的所有相关查询都找到，会综合分析；比如还有如下查询：

    `select * from task where status = 0 and type = 12 limit 10;`
    `select count(*) from task where status = 0 ;`
那么索引建立成(status,type,operator_id,operate_time)就是非常正确的，因为可以覆盖到所有情况。
这个就是利用了索引的最左匹配的原则

### 查询优化神器 - explain 命令

[参考](https://www.cnblogs.com/cxhfuujust/p/11100855.html)

EXPLAIN Output Columns

|列名|	说明|
|:----|:----|
|id	        |执行编号，标识select所属的行。如果在语句中没子查询或关联查询，只有唯一的select，每行都将显示1。否则，内层的select语句一般会顺序编号，对应于其在原始语句中的位置
|select_type|	显示本行是简单或复杂select。如果查询有任何复杂的子查询，则最外层标记为PRIMARY（DERIVED、UNION、UNION RESUlT）
|table	    |访问引用哪个表（引用某个查询，如“derived3”）
|type	    |数据访问/读取操作类型（ALL、index、range、ref、eq_ref、const/system、NULL）
|possible_keys| 	揭示哪一些索引可能有利于高效的查找
|key	    |显示mysql决定采用哪个索引来优化查询
|key_len	|显示mysql在索引里使用的字节数
|ref	    |显示了之前的表在key列记录的索引中查找值所用的列或常量
|rows	    |为了找到所需的行而需要读取的行数，估算值，不精确。通过把所有rows列值相乘，可粗略估算整个查询会检查的行数
|Extra	    |额外信息，如using index、filesort等

具体用法和字段含义可以参考[官网explain-output](https://dev.mysql.com/doc/refman/8.0/en/explain-output.html)

> rows是核心指标，绝大部分rows小的语句执行一定很快（有例外）, 所以优化语句基本上都是在优化rows。

### 慢查询优化基本步骤

> 慢查询通常是缺少索引，索引不合理或者业务代码实现所致

1. 先运行看看是否真的很慢，注意设置SQL_NO_CACHE (slow_query_log_file 开启并且查询慢查询日志)

2. where条件单表查，锁定最小返回记录表。
   这句话的意思是把查询语句的where都应用到表中返回的记录数最小的表开始查起，单表每个字段分别查询，看哪个字段的区分度最高

3. explain查看执行计划，是否与1预期一致（从锁定记录较少的表开始查询）

4. order by limit 形式的sql语句让排序的表优先查

5. 了解业务方使用场景 (调整数据修改索引；业务代码层限制不合理访问)

6. 加索引时参照建索引的几大原则

7. 观察结果，不符合预期继续从0分析

#### 几个慢查询案例

##### 1. 复杂语句写法
> 不同的语句书写方式对于效率往往有本质的差别
>
```mysql
select
   distinct cert.emp_id 
from
   cm_log cl 
inner join
   (
      select
         emp.id as emp_id,
         emp_cert.id as cert_id 
      from
         employee emp 
      left join
         emp_certificate emp_cert 
            on emp.id = emp_cert.emp_id 
      where
         emp.is_deleted=0
   ) cert 
      on (
         cl.ref_table='Employee' 
         and cl.ref_oid= cert.emp_id
      ) 
      or (
         cl.ref_table='EmpCertificate' 
         and cl.ref_oid= cert.cert_id
      ) 
where
   cl.last_upd_date >='2013-11-07 15:03:00' 
   and cl.last_upd_date<='2013-11-08 16:00:00';
```
1. 先运行一下，53条记录 1.87秒，又没有用聚合语句，比较慢

2. explain

3. 简述一下执行计划，首先mysql根据idx_last_upd_date索引扫描cm_log表获得379条记录；
  然后查表扫描了63727条记录，分为两部分，derived表示构造表，也就是不存在的表，可以简单理解成是一个语句形成的结果集，后面的数字表示语句的ID。
  derived2表示的是ID = 2的查询构造了虚拟表，并且返回了63727条记录。
  我们再来看看ID = 2的语句究竟做了写什么返回了这么大量的数据，
  首先全表扫描employee表13317条记录，
  然后根据索引emp_certificate_empid关联emp_certificate表，
  rows = 1表示，每个关联都只锁定了一条记录，效率比较高。
  获得后，再和cm_log的379条记录根据规则关联。
  从执行过程上可以看出返回了太多的数据，返回的数据绝大部分cm_log都用不到，因为cm_log只锁定了379条记录。

4. 如何优化呢？可以看到我们在运行完后还是要和cm_log做join,那么我们能不能之前和cm_log做join呢？
  基本思想是如果cm_log的ref_table是EmpCertificate就关联emp_certificate表，
  如果ref_table是Employee就关联employee表，我们完全可以拆成两部分，并用union连接起来，注意这里用union，而不用union all
  因为原语句有“distinct”来得到唯一的记录，而union恰好具备了这种功能。

优化过的语句如下：

```mysql
select
   emp.id 
from
   cm_log cl 
inner join
   employee emp 
      on cl.ref_table = 'Employee' 
      and cl.ref_oid = emp.id  
where
   cl.last_upd_date >='2013-11-07 15:03:00' 
   and cl.last_upd_date<='2013-11-08 16:00:00' 
   and emp.is_deleted = 0  
union
select
   emp.id 
from
   cm_log cl 
inner join
   emp_certificate ec 
      on cl.ref_table = 'EmpCertificate' 
      and cl.ref_oid = ec.id  
inner join
   employee emp 
      on emp.id = ec.emp_id  
where
   cl.last_upd_date >='2013-11-07 15:03:00' 
   and cl.last_upd_date<='2013-11-08 16:00:00' 
   and emp.is_deleted = 0
```

##### 2. 明确应用场景

对列的区分度的认知，一般上我们认为区分度越高的列，越容易锁定更少的记录，但在一些特殊的情况下，这种理论是有局限性的。

```mysql
select * from stage_poi sp 
where
   sp.accurate_result=1 
   and (
      sp.sync_status=0 
      or sp.sync_status=2 
      or sp.sync_status=4
   );
```

1. 先看看运行多长时间,951条数据 6.22秒，真的很慢

2. 先explain，rows达到了361万，type = ALL表明是全表扫描。

3. 所有字段都应用查询返回记录数，因为是单表查询 0已经做过了951条。

4. 让explain的rows 尽量逼近951。

5. 看一下accurate_result = 1的记录数：

`select count(*),accurate_result from stage_poi group by accurate_result;`

```
+----------+-----------------+
| count(*) | accurate_result |
+----------+-----------------+
|     1023 |              -1 |
|  2114655 |               0 |
|   972815 |               1 |
+----------+-----------------+
```

我们看到accurate_result这个字段的区分度非常低，整个表只有-1,0,1三个值，加上索引也无法锁定特别少量的数据。

再看一下sync_status字段的情况：`select count(*),sync_status from stage_poi  group by sync_status; `
```
+----------+-------------+
| count(*) | sync_status |
+----------+-------------+
|     3080 |           0 |
|  3085413 |           3 |
+----------+-------------+
```

> 区分度也很低，根据理论，也不适合建立索引。

问题分析到这，好像得出了这个表无法优化的结论，两个列的区分度都很低，即便加上索引也只能适应这种情况，很难做普遍性的优化，比如当sync_status 0、3分布的很平均，那么锁定记录也是百万级别的。

4. 找业务方去沟通，看看使用场景。业务方是这么来使用这个SQL语句的，每隔五分钟会扫描符合条件的数据，处理完成后把sync_status这个字段变成1, 五分钟符合条件的记录数并不会太多，1000个左右。

 了解了业务方的使用场景后，优化这个SQL就变得简单了，因为业务方保证了数据的不平衡，如果加上索引可以过滤掉绝大部分不需要的数据。

5. 根据建立索引规则，使用如下语句建立索引 `alter table stage_poi add index idx_acc_status(accurate_result,sync_status);`

6. 观察预期结果,发现只需要200ms，快了30多倍。

单表查询相对来说比较好优化，大部分时候只需要把where条件里面的字段依照规则加上索引就好，如果只是这种“无脑”优化的话，显然一些区分度非常低的列，不应该加索引的列也会被加上索引，这样会对插入、更新性能造成严重的影响，同时也有可能影响其它的查询语句。

所以我们第4步调差SQL的使用场景非常关键，我们只有知道这个业务场景，才能更好地辅助我们更好的分析和优化查询语句。

##### 3. 无法优化的语句

```mysql
select c.id, c.name, c.position, c.sex, c.phone, c.office_phone, c.feature_info, c.birthday,
   c.creator_id, c.is_keyperson, c.giveup_reason, c.status, c.data_source,
   from_unixtime(c.created_time) as created_time,
   from_unixtime(c.last_modified) as last_modified,
   c.last_modified_user_id  
from
   contact c  
inner join
   contact_branch cb 
      on  c.id = cb.contact_id  
inner join
   branch_user bu 
      on  cb.branch_id = bu.branch_id 
      and bu.status in (
         1,
      2)  
   inner join
      org_emp_info oei 
         on  oei.data_id = bu.user_id 
         and oei.node_left >= 2875 
         and oei.node_right <= 10802 
         and oei.org_category = - 1  
   order by
      c.created_time desc  limit 0 ,
      10;
```

1. 先看语句运行多长时间，10条记录用了13秒，已经不可忍受。

2. explain
```
+----+-------------+-------+--------+-------------------------------------+-------------------------+---------+--------------------------+------+----------------------------------------------+
| id | select_type | table | type   | possible_keys                       | key                     | key_len | ref                      | rows | Extra                                        |
+----+-------------+-------+--------+-------------------------------------+-------------------------+---------+--------------------------+------+----------------------------------------------+
|  1 | SIMPLE      | oei   | ref    | idx_category_left_right,idx_data_id | idx_category_left_right | 5       | const                    | 8849 | Using where; Using temporary; Using filesort |
|  1 | SIMPLE      | bu    | ref    | PRIMARY,idx_userid_status           | idx_userid_status       | 4       | meituancrm.oei.data_id   |   76 | Using where; Using index                     |
|  1 | SIMPLE      | cb    | ref    | idx_branch_id,idx_contact_branch_id | idx_branch_id           | 4       | meituancrm.bu.branch_id  |    1 |                                              |
|  1 | SIMPLE      | c     | eq_ref | PRIMARY                             | PRIMARY                 | 108     | meituancrm.cb.contact_id |    1 |                                              |
+----+-------------+-------+--------+-------------------------------------+-------------------------+---------+--------------------------+------+----------------------------------------------+
```
从执行计划上看，mysql先查org_emp_info表扫描8849记录，再用索引idx_userid_status关联branch_user表，再用索引idx_branch_id关联contact_branch表，最后主键关联contact表。

rows返回的都非常少，看不到有什么异常情况。我们在看一下语句，发现后面有order by + limit组合，会不会是排序量太大搞的？

于是我们简化SQL，去掉后面的order by 和 limit，看看到底用了多少记录来排序。

select
  count(*)
from
   contact c  
inner join
   contact_branch cb 
      on  c.id = cb.contact_id  
inner join
   branch_user bu 
      on  cb.branch_id = bu.branch_id 
      and bu.status in (
         1,
      2)  
   inner join
      org_emp_info oei 
         on  oei.data_id = bu.user_id 
         and oei.node_left >= 2875 
         and oei.node_right <= 10802 
         and oei.org_category = - 1  
+----------+
| count(*) |
+----------+
|   778878 |
+----------+
1 row in set (5.19 sec)
发现排序之前居然锁定了778878条记录，如果针对70万的结果集排序，将是灾难性的，怪不得这么慢，那我们能不能换个思路，先根据contact的created_time排序，再来join会不会比较快呢？

于是改造成下面的语句，也可以用straight_join来优化：

select
   c.id,
   c.name,
   c.position,
   c.sex,
   c.phone,
   c.office_phone,
   c.feature_info,
   c.birthday,
   c.creator_id,
   c.is_keyperson,
   c.giveup_reason,
   c.status,
   c.data_source,
   from_unixtime(c.created_time) as created_time,
   from_unixtime(c.last_modified) as last_modified,
   c.last_modified_user_id   
from
   contact c  
where
   exists (
      select
         1 
      from
         contact_branch cb  
      inner join
         branch_user bu        
            on  cb.branch_id = bu.branch_id        
            and bu.status in (
               1,
            2)      
         inner join
            org_emp_info oei           
               on  oei.data_id = bu.user_id           
               and oei.node_left >= 2875           
               and oei.node_right <= 10802           
               and oei.org_category = - 1      
         where
            c.id = cb.contact_id    
      )    
   order by
      c.created_time desc  limit 0 ,
      10;
      
验证一下效果 预计在1ms内，提升了13000多倍！

10 rows in set (0.00 sec)

本以为至此大工告成，但我们在前面的分析中漏了一个细节，先排序再join和先join再排序理论上开销是一样的，

为何提升这么多是因为有一个limit！大致执行过程是：mysql先按索引排序得到前10条记录，然后再去join过滤，当发现不够10条的时候，再次去10条，再次join，这显然在内层join过滤的数据非常多的时候，将是灾难的，极端情况，内层一条数据都找不到，mysql还傻乎乎的每次取10条，几乎遍历了这个数据表！

用不同参数的SQL试验下：

select
   sql_no_cache   c.id,
   c.name,
   c.position,
   c.sex,
   c.phone,
   c.office_phone,
   c.feature_info,
   c.birthday,
   c.creator_id,
   c.is_keyperson,
   c.giveup_reason,
   c.status,
   c.data_source,
   from_unixtime(c.created_time) as created_time,
   from_unixtime(c.last_modified) as last_modified,
   c.last_modified_user_id    
from
   contact c   
where
   exists (
      select
         1        
      from
         contact_branch cb         
      inner join
         branch_user bu                     
            on  cb.branch_id = bu.branch_id                     
            and bu.status in (
               1,
            2)                
         inner join
            org_emp_info oei                           
               on  oei.data_id = bu.user_id                           
               and oei.node_left >= 2875                           
               and oei.node_right <= 2875                           
               and oei.org_category = - 1                
         where
            c.id = cb.contact_id           
      )        
   order by
      c.created_time desc  limit 0 ,
      10;
Empty set (2 min 18.99 sec)

2 min 18.99 sec！比之前的情况还糟糕很多。

由于mysql的nested loop机制，遇到这种情况，基本是无法优化的。

这条语句最终也只能交给应用系统去优化自己的逻辑了。

通过这个例子我们可以看到，并不是所有语句都能优化，而往往我们优化时，由于SQL用例回归时落掉一些极端情况，会造成比原来还严重的后果。

第一：不要指望所有语句都能通过SQL优化，
第二：不要过于自信，只针对具体case来优化，而忽略了更复杂的情况。

慢查询的案例就分析到这儿，以上只是一些比较典型的案例。我们在优化过程中遇到过超过1000行，涉及到16个表join的“垃圾SQL”，

也遇到过线上线下数据库差异导致应用直接被慢查询拖死，也遇到过varchar等值比较没有写单引号，
还遇到过笛卡尔积查询直接把从库搞死。
再多的案例其实也只是一些经验的积累，如果我们熟悉查询优化器、索引的内部原理，那么分析这些案例就变得特别简单了。

写在后面的话
本文以一个慢查询案例引入了MySQL索引原理、优化慢查询的一些方法论;并针对遇到的典型案例做了详细的分析。其实做了这么长时间的语句优化后才发现，

任何数据库层面的优化都抵不上应用系统的优化，同样是MySQL，可以用来支撑Google/FaceBook/Taobao应用，但可能连你的个人网站都撑不住。

套用最近比较流行的话：“查询容易，优化不易，且写且珍惜！”

参考文献：
1.《高性能MySQL》 
2.《数据结构与算法分析》
