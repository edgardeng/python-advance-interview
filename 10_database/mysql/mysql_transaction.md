# MySQL 事务
> MySQL 事务主要用于处理操作量大，复杂度高的数据。
> 比如说，在人员管理系统中，你删除一个人员，你既需要删除人员的基本资料，也要删除和该人员相关的信息，如信箱，文章等等，这样，这些数据库操作语句就构成一个事务！

在 MySQL 中只有使用了 Innodb 数据库引擎的数据库或表才支持事务。
事务处理可以用来维护数据库的完整性，保证成批的 SQL 语句要么全部执行，要么全部不执行。
事务用来管理 insert,update,delete 语句
一般来说，事务是必须满足4个条件（ACID）：：原子性（Atomicity，或称不可分割性）、一致性（Consistency）、隔离性（Isolation，又称独立性）、持久性（Durability）。

* 原子性：一个事务（transaction）中的所有操作，要么全部完成，要么全部不完成，不会结束在中间某个环节。事务在执行过程中发生错误，会被回滚（Rollback）到事务开始前的状态，就像这个事务从来没有执行过一样。

* 一致性：在事务开始之前和事务结束以后，数据库的完整性没有被破坏。这表示写入的资料必须完全符合所有的预设规则，这包含资料的精确度、串联性以及后续数据库可以自发性地完成预定的工作。

* 隔离性：数据库允许多个并发事务同时对其数据进行读写和修改的能力，隔离性可以防止多个事务并发执行时由于交叉执行而导致数据的不一致。事务隔离分为不同级别，包括读未提交（Read uncommitted）、读提交（read committed）、可重复读（repeatable read）和串行化（Serializable）。

* 持久性：事务处理结束后，对数据的修改就是永久的，即便系统故障也不会丢失。

在 MySQL 命令行的默认设置下，事务都是自动提交的，即执行 SQL 语句后就会马上执行 COMMIT 操作。因此要显式地开启一个事务务须使用命令 BEGIN 或 START TRANSACTION，或者执行命令 SET AUTOCOMMIT=0，用来禁止使用当前会话的自动提交。

事务控制语句：

BEGIN 或 START TRANSACTION 显式地开启一个事务；

COMMIT 也可以使用 COMMIT WORK，不过二者是等价的。COMMIT 会提交事务，并使已对数据库进行的所有修改成为永久性的；

ROLLBACK 也可以使用 ROLLBACK WORK，不过二者是等价的。回滚会结束用户的事务，并撤销正在进行的所有未提交的修改；

SAVEPOINT identifier，SAVEPOINT 允许在事务中创建一个保存点，一个事务中可以有多个 SAVEPOINT；

RELEASE SAVEPOINT identifier 删除一个事务的保存点，当没有指定的保存点时，执行该语句会抛出一个异常；

ROLLBACK TO identifier 把事务回滚到标记点；

SET TRANSACTION 用来设置事务的隔离级别。InnoDB 存储引擎提供事务的隔离级别有READ UNCOMMITTED、READ COMMITTED、REPEATABLE READ 和 SERIALIZABLE。

MYSQL 事务处理主要有两种方法：

1、用 BEGIN, ROLLBACK, COMMIT来实现

BEGIN 开始一个事务
ROLLBACK 事务回滚
COMMIT 事务确认

2、直接用 SET 来改变 MySQL 的自动提交模式:

SET AUTOCOMMIT=0 禁止自动提交
SET AUTOCOMMIT=1 开启自动提交
事务测试
mysql> use RUNOOB;
Database changed
mysql> CREATE TABLE runoob_transaction_test( id int(5)) engine=innodb;  # 创建数据表
Query OK, 0 rows affected (0.04_object_oriented sec)
 
mysql> select * from runoob_transaction_test;
Empty set (0.01 sec)
 
mysql> begin;  # 开始事务
Query OK, 0 rows affected (0.00 sec)
 
mysql> insert into runoob_transaction_test value(5);
Query OK, 1 rows affected (0.01 sec)
 
mysql> insert into runoob_transaction_test value(6);
Query OK, 1 rows affected (0.00 sec)
 
mysql> commit; # 提交事务
Query OK, 0 rows affected (0.01 sec)
 
mysql>  select * from runoob_transaction_test;
+------+
| id   |
+------+
| 5    |
| 6    |
+------+
2 rows in set (0.01 sec)
 
mysql> begin;    # 开始事务
Query OK, 0 rows affected (0.00 sec)
 
mysql>  insert into runoob_transaction_test values(7);
Query OK, 1 rows affected (0.00 sec)
 
mysql> rollback;   # 回滚
Query OK, 0 rows affected (0.00 sec)
 
mysql>   select * from runoob_transaction_test;   # 因为回滚所以数据没有插入
+------+
| id   |
+------+
| 5    |
| 6    |
+------+
2 rows in set (0.01 sec)
 
mysql>


在用户操作MySQL过程中，对于一般简单的业务逻辑或中小型程序而言，无需考虑应用MySQL事务。但在比较复杂的情况下，往往用户在执行某些数据操作过程中，需要通过一组SQL语句执行多项并行业务逻辑或程序，这样，就必须保证所用命令执行的同步性。使执行序列中，产生依靠关系的动作能够同时操作成功或同时返回初始状态。在此情况下，就需要用户优先考虑使用MySQL事务处理。

在MySQL中，事务由单独单元的一个或多个SQL语句组成。在这个单元中，每个MySQL语句是相互依赖的。而整个单独单元作为一个不可分割的整体，如果单元中某条SQL语句一旦执行失败或产生错误，整个单元将会回滚。所有受到影响的数据将返回到事务开始以前的状态；如果单元中的所有SQL语句均执行成功，则事务被顺利执行。

通过InnoDB和BDB类型表，MySQL事务能够完全满足事务安全的ACID测试，但是并不是所有表类型都支持事务，如MyISAM类型表就不能支持事务，只能通过伪事务对表实现事务处理。

MySQL事务的创建与存在周期

创建事务

创建事务的一般过程是：初始化事务、创建事务、应用SELECT语句查询数据是否被录入和提交事务。如果用户不在操作数据库完成后执行事务提交，则系统会默认执行回滚操作。如果用户在提交事务前选择撤销事务，则用户在撤销前的所有事务将被取消，数据库系统会回到初始状态。

默认情况下，在MySQL中创建的数据表类型都是MyISAM，但是该类型的数据表并不能支持事务。所以，如果用户想让数据表支持事务处理能力，必须将当前操作数据表的类型设置为InnoDB或BDB。

在创建事务的过程中，用户需要创建一个InnoDB或BDB类型的数据表，其基本命令结构如下：

CREATE TABLE table_name（field-defintions）TYPE=INNODB/BDB；

其中，table_name为表名，而field_defintions为表内定义的字段等属性，TYPE为数据表的类型，既可以是InnoDB类型，同样也可以是BDB类型。

当用户希望已经存在的表支持事务处理，则可以应用ALTER TABLE命令指定数据表的类型实现对表的类型更改操作，使原本不支持事务的数据表更改为支持事务处理的类型。其命令如下：

ALTER TABLE table_name TYPE=INNODB/BDB；

当用户更改完表的类型后，即可使数据表支持事务处理。

应用ALTER TABLE操作可能会导致数据库中数据丢失，因此为了避免非预期结果出现，在使用ALTER TABLE命令之前，用户需要创建一个表备份。

初始化事务

初始化MySQL事务，首先声明初始化MySQL事务后所有的SQL语句为一个单元。在MySQL中，应用START TRANSACTION命令来标记一个事务的开始。初始化事务的结构如下：

START TRANSACTION；

另外，用户也可以使用BEGIN或者BEGIN WORK命令初始化事务，通常START TRANSACTION命令后面跟随的是组成事务的SQL语句。

在命令提示符中输入如下命令：

start transaction；

如果在用户输入以上代码后，MySQL数据库没有给出警告提示或返回错误信息，则说明事务初始化成功，用户可以继续执行下一步操作。

创建事务

insert into connection（email, cellphone, QQ, sid）

values（'barrystephen@126.com'，13456000000，187034000，3）；

应用SELECT语句查看数据是否被正确输入

SELECT * FROM connection WHERE sid=3；

ps:在用户插入新表为"InnoDB"类型或更改原来表类型为"InnoDB"时，如果在输入命令提示后，MySQL提示"The 'InnoDB' feature is disabled；you needInnoDB' to have it working"警告，则说明InnoDB表类型并没有被开启，用户需要找到MySQL文件目录下的"my.ini"文件，定位"skip_innodb"选项位置，将原来的"skip_innodb"改为"#skip_innodb"后保存该文件，重新启动MySQL服务器，即可令数据库支持"InnoDB"类型表。 

提交事务

在用户没有提交事务之前，当其他用户连接MySQL服务器时，应用SELECT语句查询结果，则不会显示没有提交的事务。当且仅当用户成功提交事务后，其他用户才可能通过SELECT语句查询事务结果，由事务的特性可知，事务具有孤立性，当事务处在处理过程中，其实MySQL并未将结果写入磁盘中，这样一来，这些正在处理的事务相对其他用户是不可见的。一旦数据被正确插入，用户可以使用COMMIT命令提交事务。提交事务的命令结构如下：

COMMIT

一旦当前执行事务的用户提交当前事务，则其他用户就可以通过会话查询结果。

撤销事务（事务回滚）

撤销事务，又被称作事务回滚。即事务被用户开启、用户输入的SQL语句被执行后，如果用户想要撤销刚才的数据库操作，可使用ROLLBACK命令撤销数据库中的所有变化。ROLLBACK命令结构如下：

ROLLBACK

输入回滚操作后，如何判断是否执行回滚操作了呢？可以通过SELECT语句查看11.2.2小节中插入的数据是否存在.

如果执行一个回滚操作，则在输入START TRANSACTIONA命令后的所有SQL语句都将执行回滚操作。故在执行事务回滚前，用户需要慎重选择执行回滚操作。如果用户开启事务后，没有提交事务，则事务默认为自动回滚状态，即不保存用户之前的任何操作。

事务的存在周期

事务的周期由用户在命令提示符中输入START TRANSACTION指令开始，直至用户输入COMMIT结束.

事务不支持嵌套功能，当用户在未结束第一个事务又重新打开一个事务，则前一个事务会自动提交，同样MySQL命令中很多命令都会隐藏执行COMMIT命令。

MySQL行为

在MySQL中，存在两个可以控制行为的变量，它们分别是AUTOCOMMIT变量和TRANSACTION ISOLACTION LEVEL变量。

自动提交

在MySQL中，如果不更改其自动提交变量，则系统会自动向数据库提交结果，用户在执行数据库操作过程中，不需要使用START TRANSACTION语句开始事务，应用COMMIT或者ROLLBACK提交事务或执行回滚操作。如果用户希望通过控制MySQL自动提交参数，可以更改提交模式，这一更改过程是通过设置AUTOCOMMIT变量来实现。

下面通过一个示例向读者展示如何关闭自动提交参数。在命令提示符中输入以下命令：

SET AUTOCOMMIT=0；

只有当用户输入COMMIT命令后，MySQL才将数据表中的资料提交到数据库中，如果不提交事务，而终止MySQL会话，数据库将会自动执行回滚操作。

可以通过查看"@@AUTOCOMMIT"变量来查看当前自动提交状态，查看此变量SELECT @@AUTOCOMMIT。

事务的隔离级别

基于ANSI/ISO SQL规范，MySQL提供4种孤立级：

SERIALIZABLE（序列化）

REPEATABLE READ（可重读）

READ COMMITTED（提交后读）

READ UNCOMMITTED（未提交读）

在MySQL中，可以使用TRANSACTION ISOLATION LEVEL变量来修改事务孤立级，其中，MySQL的默认隔离级别为REPEATABLE READ（可重读），用户可以使用SELECT命令获取当前事务孤立级变量的值，其命令如下：

SELECT @@tx_isolation；

如果用户想要修改事务的隔离级别，必须首先获取SUPER优先权，以便用户可以顺利执行修改操作，set。

事务的使用技巧和注意事项

应用小事务，保证每个事务不会在执行前等待很长时间，从而避免各个事务因为互相等待而导致系统性能的大幅度下降。

选择合适的孤立级，因为事务的性能与其对服务器产生的负载成反比，即当事务孤立级越高，其性能越低，但是其安全性也越高。只有选择适当的孤立级，才能有效地提高MySQL系统性能和应用性。

死锁的概念与避免，即当两个或者多个处于不同序列的用户打算同时更新某相同的数据库时，因互相等待对方释放权限而导致双方一直处于等待状态。在实际应用中，两个不同序列的客户打算同时对数据执行操作，极有可能产生死锁。更具体地讲，当两个事务相互等待操作对方释放所持有的资源，而导致两个事务都无法操作对方持有的资源，这样无限期的等待被称作死锁。MySQL的InnoDB表处理程序具有检查死锁这一功能，如果该处理程序发现用户在操作过程中产生死锁，该处理程序立刻通过撤销操作来撤销其中一个事务，以便使死锁消失。这样就可以使另一个事务获取对方所占有的资源而执行逻辑操作。

MySQL伪事务

在MySQL中，InnoDB和BDB类型表可以支持事务处理，但是MySQL中MyISAM类型表并不能支持事务处理，对于某些应用该类型的数据表，用户可以选择应用表锁定来替代事务。这种引用表锁定来替代事务的事件被称作伪事务。使用表锁定来锁定表的操作，可以加强非事务表在执行过程的安全性和稳定性。

用表锁定代替事务

在MySQL的MyISAM类型数据表中，并不支持COMMIT（提交）和ROLLBACK（回滚）命令。当用户对数据库执行插入、删除、更新等操作时，这些变化的数据都被立刻保存在磁盘中。这样，在多用户环境中，会导致诸多问题。为了避免同一时间有多个用户对数据库中指定表进行操作，可以应用表锁定来避免在用户操作数据表过程中受到干扰。当且仅当该用户释放表的操作锁定后，其他用户才可以访问这些修改后的数据表。

设置表锁定代替事务基本步骤如下：

（1）为指定数据表添加锁定。其语法如下：

LOCK TABLES table_name lock_type，……

其中，table_name为被锁定的表名，lock_type为锁定类型，该类型包括以读方式（READ）锁定表，以写方式（WRITE）锁定表。

（2）用户执行数据表的操作，可以添加、删除或者更改部分数据。

（3）用户完成对锁定数据表的操作后，需要对该表进行解锁操作，释放该表的锁定状态。其语法如下：

UNLOCK TABLES

以读方式锁定数据表，该方式是设置锁定用户的其他方式操作，如删除、插入、更新都不被允许，直至用户进行解锁操作。

lock table studentinfo read；

其中的lock_type参数中，用户指定数据表以读方式（READ）锁定数据表的变体为READ LOCAL锁定，其与READ锁定的不同点是，该参数所指定的用户会话可以执行INSERT操作，它是为了使用MySQL dump工具而创建的一种变体形式。

以写方式锁定数据表，该方式是是设置用户可以修改数据表中的数据，但是除自己以外其他会话中的用户不能进行任何读操作。在命令提示符中输入如下命令：

lock table studentinfo write；

当数据表被释放锁定后，其他访问数据库的用户即可查看数据表的内容。

应用表锁实现伪事务

通过使用表锁定对MyISAM表进行锁定操作，以此过程来代替事务型表InnoDB，即应用表锁定来实现伪事务。实现伪事务的一般步骤如下：

（1）对数据库中的数据表进行锁定操作，可以对多个表做不同的方式锁定，其代码格式如下：

LOCK TABLE table_name1 lock_type1，table_name2 lock_type2，……

（2）执行数据库操作，向锁定的数据表中执行添加、删除、修改操等操作。

如前面提到的INSERT、UPDATE、DELETE等操作。用户可以对锁定的数据表执行上述操作，在执行过程中，该伪事务所产生的结果是不会被其他用户更改的。

（3）释放锁定的数据表，以便让正在队列中等待查看或操作的其他用户可以浏览数据表中的数据或对操作表执行各种数据的操作。

如果存在其他会话要求访问已锁定的多个表格，则该会话必须被迫等待当前锁定用户释放锁定表。才允许其他会话访问该数据表，表锁定使不同会话执行的数据库操作彼此独立。应用数据表锁定方式可以使不支持事务类型的表实现伪事务。

Python 执行 MySQL 事务

一、MySQL 事务

事务就是指逻辑上的一组 SQL 操作，组成这组操作的各个 SQL 语句，执行时要么全成功要么全失败。

举个例子，小明给小红转账100元，转账过程实际上就是小明的账户减少100元，小红的账户增加100元，对应的SQL语句为：

update account set money=money-5 where name='xiaoming';

update account set money=money+5 where name='xiaohong';

上述的两条SQL操作，在事务中的操作就是要么都执行成功，要么都执行失败，如果只有第一条成功，那么小明就损失100元，而小红并没有收到100元，这是不可取的，所以这就是事务，事务就是指逻辑上的一组SQL 操作，组成这组操作的各个 SQL 语句，执行时要么全成功要么全失败。事务处理可以用来维护数据库的完整性，保证成批的 SQL 语句要么全部执行，要么全部不执行，在 MySQL 中只有使用了 Innodb 库引擎的数据库或表才支持事务，所以很多情况下我们都使用 Innodb 引擎.

事务的特性如下：

原子性：事务是一个不可分割的单位，事务中的所有 SQL 操作要么都成功，要么都失败

一致性：事务发生前和发生后，数据的完整性必须保持一致

隔离性：当并发访问数据库时，一个正在执行的事务在执行完毕前，对于其它的会话是不可见的，多个并发事务之间的数据是相互隔离的

持久性：一个事务一旦被提交，它对数据库中的数据改变就是永久性的，如果出了错误，事务也不允许撤销，只能通过 "补偿性事务"

mysql> begin # 开启事务
mysql> rollback # 回滚事务
mysql> commit # 提交事务

数据库默认事务是自动提交的，也就是说，当我们执行 select，insert，update，delete 等操作时，就会自动提交事务，如果关闭事务的自动提交，那么我们执行完 select，insert，update，delete 操作后需要再执行 commit 来提交事务，否则就不会执行

二、游标

游标是系统为用户开设的一个数据缓冲区，存放 SQL 语句的执行结果，用法如下：

In [1]: import pymysql

In [2]: c = MySQLdb.connect(user='root', passwd='root', db='test') # 连接数据库

In [3]: cus = c.cursor() # 创建一个游标对象

In [4]: cus.execute('select * from user;') # 使用execute()方法可以执行SQL语句，执行后的结果会存在缓冲区
Out[4]: 4L

In [5]: result1 = cus.fetchone() # 可以使用fetchone()来查看缓冲区的一条记录

In [6]: result2 = cus.fetchmany(3) # 可以使用fetchmany()来查看缓冲区的多条记录

In [7]: result3 = cus.fetchall() # 可以使用fetchall()来查看所有的记录

三、根据游标执行 MySQL 事务

#!/usr/bin/env python
import pymysql

def connect_mysql():
db_config = {
'host': '127.0.0.1',
'port': 3306,
'user': 'root',
'passwd': 'pzk123'
}
c = pymysql.connect(**db_config)
return c

if __name__ == '__main__':
c = connect_mysql() # 首先连接数据库
cus = c.cursor() # 生成游标对象
sql = 'drop database test;' # 定义要执行的SQL语句
try:
cus.execute(sql) # 执行SQL语句
c.commit() # 如果执行成功就提交事务
except Exception as e: 
c.rollback() # 如果执行失败就回滚事务
raise e
finally:
c.close() # 最后记得关闭数据库连接
