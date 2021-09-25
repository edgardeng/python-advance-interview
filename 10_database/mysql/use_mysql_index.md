## MySQL 索引的使用

### 单列索引
> 一个索引只包含单个列，一个表可以有多个单列索引，但这不是组合索引；

* 创建索引 `CREATEINDEXindex_name ON mytable(username(length));`

 如果是 CHAR，VARCHAR类型，length可以小于字段实际长度;
  如果是BLOB和TEXT类型，必须指定 length，下同。

* 修改表结构 `ALTERmytableADDINDEX[index_name] ON (username(length)) `

* 创建表的时候直接指定 `CREATE TABLE mytable( ID INT NOT NULL, usernameVARCHAR(16) NOT NULL, INDEX [index_name] (username(length)) );`

* 删除索引的语法： `DROP INDEX [index_name] ON mytable; `

* 创建唯一索引 `CREATEUNIQUEINDEX index_name ON mytable(username(length)) `
    > 索引列的值必须唯一，但允许有空值
                                                                          >
* 修改表结构 `ALTERmytableADDUNIQUE[index_name] ON (username(length))`

* 创建表的时候直接指定 `CREATE TABLE mytable( ID INT NOT NULL, usernameVARCHAR(16) NOT NULL,UNIQUE[index_name] (username(length)) );`

* 创建主键索引 `CREATE TABLE mytable( ID INT NOT NULL, username VARCHAR(16) NOT NULL, PRIMARY KEY(ID) );`
  > 特殊的唯一索引，不允许有空值 当然也可以用ALTER命令。记住：一个表只能有一个主键。


 为了形象地对比单列索引和组合索引，为表添加多个字段：

 CREATE TABLE mytable( ID INT NOT NULL, username VARCHAR(16) NOT NULL, city VARCHAR(50) NOT NULL, age INT NOT NULL );

 为了进一步榨取MySQL的效率，就要考虑建立组合索引。就是将 name, city, age建到一个索引里：

 ALTER TABLE mytableADDINDEX name_city_age (name(10),city,age);

 建表时，usernname长度为 16，这里用 10。这是因为一般情况下名字的长度不会超过10，这样会加速索引查询速度，还会减少索引文件的大小，提高 INSERT的更新速度。

 如果分别在 usernname，city，age上建立单列索引，让该表有3个单列索引，查询时和上述的组合索引效率也会大不一样，远远低于我们的组合索引。虽然此时有了三个索引，但MySQL只能用到其中的那个它认为似乎是最有效率的单列索引。

 建立这样的组合索引，其实是相当于分别建立了下面三组组合索引：

　　 usernname,city,age usernname,city usernname

 为什么没有 city，age这样的组合索引呢?这是因为MySQL组合索引“最左前缀”的结果。简单的理解就是只从最左面的开始组合。并不是只要包含这三列的查询都会用到该组合索引，下面的几个SQL就会用到这个组合索引：

SELECT* FROM mytable WHREE username="admin" AND city="郑州" 　　SELECT * FROM mytable WHREE username="admin"

 而下面几个则不会用到：

 　　SELECT * FROM mytable WHREE age=20 AND city="郑州" 　　SELECT * FROM mytable WHREE city="郑州"

(5)建立索引的时机

　　 到这里我们已经学会了建立索引，那么我们需要在什么情况下建立索引呢?
一般来说，在WHERE和JOIN中出现的列需要建立索引
，但也不完全如此，因为MySQL只对<，<=，=，>，>=，BETWEEN，IN，以及某些时候的LIKE才会使用索引
。例如：

 SELECT t.Name FROM mytable t LEFT JOIN mytable m ON t.Name=m.username WHERE m.age=20 AND m.city='郑州'

 此时就需要对city和age建立索引，由于mytable表的 userame也出现在了JOIN子句中，也有对它建立索引的必要。

 刚才提到只有某些时候的LIKE才需建立索引。
因为在以通配符%和_开头作查询时，MySQL不会使用索引。例如下句会使用索引：

 　　SELECT * FROM mytable WHERE username like'admin%'

 而下句就不会使用：

　　 SELECT * FROM mytable WHEREt Name like'%admin'

 因此，在使用LIKE时应注意以上的区别。

#### 索引的不足之处

* 降低更新表的速度，如对表进行 INSERT、UPDATE和DELETE
 > 因为更新表时，MySQL不仅要保存数据，还要保存一下索引文件。
* 建立索引会占用磁盘空间的索引文件。一般情况这个问题不太严重，但如果你在一个大表上创建了多种组合索引，索引文件的会膨胀很快。


### 联合索引
> 组合索引，即一个索包含多个列
>
>
#### 最左原则

1. 组合索引多字段是有序的，并且是个完整的BTree 索引，有最左原则

2. 多列索引是先按照第一列进行排序，然后在第一列排好序的基础上再对第二列排序，
   如果没有第一列的话，直接访问第二列，那第二列肯定是无序的，直接访问后面的列就用不到索引了。

3. 搜索需要从根节点出发，上层节点对应靠左的值，搜索需要从根节点出发，否则不从根节点出发，后面的节点对应下层的值，依旧是乱序的，需要遍历，所以索引就失效了，所以有最左原则。

#### 组合索引的使用：

* 创建索引 `create index group_index_a_b on my_table(a, b); ` 
* 修改索引 `ALTER TABLE my_table ADD INDEX group_index_a_b_c (a,b,c);`

**从前往后依次使用生效，如果中间某个索引没有使用，那么断点前面的索引部分起作用，断点后面的索引没有起作用**

例如组合索引（a,b,c），

* `where a=3 and b=45 and c=5 `  这种三个索引顺序使用中间没有断点，全部发挥作用；

* `where a=3 and c=5 ` 这种情况下b就是断点，a发挥了效果，c没有效果

* `where b=3 and c=4 ` 这种情况下a就是断点，在a后面的索引都没有发挥作用，这种写法联合索引没有发挥任何效果；

* `where b=45 and a=3 and c=5 ` 全部发挥作用，abc只要用上了就行，跟写的顺序无关

* `select * from mytable where a=3 and b>7 and c=3;` (范围值就算是断点) a用到了，b也用到了，c没有用到

* `select * from mytable where a>4 and b=7 and c=9; ` a用到了 b没有使用，c没有使用

* `select * from mytable where a=3 order by b;` a用到了索引，b在结果排序中也用到了索引的效果，前面说了，a下面任意一段的b是排好序的

* `select * from mytable where a=3 order by c; ` a用到了索引，但是这个地方c没有发挥排序效果，因为中间断点了，使用 explain 可以看到 filesort

* `select * from mytable where b=3 order by a; ` b没有用到索引，排序中a也没有发挥索引效果
