# Redis
> REmote DIctionary Server(Redis) 是一个由Salvatore Sanfilippo写的key-value存储系统。

> Redis是一个开源的使用ANSI C语言编写、遵守BSD协议、支持网络、可基于内存亦可持久化的日志型、Key-Value数据库，并提供多种语言的API。

Redis, 通常被称为数据结构服务器，因为值（value）可以是 字符串(String), 哈希(Hash), 列表(list), 集合(sets) 和 有序集合(sorted sets)等类型。

## Redis 与其他 key - value 缓存产品有以下三个特点：

1. Redis支持数据的持久化，可以将内存中的数据保存在磁盘中，重启的时候可以再次加载进行使用。
2. Redis不仅仅支持简单的key-value类型的数据，同时还提供list，set，zset，hash等数据结构的存储。
3. Redis支持数据的备份，即master-slave模式的数据备份。

## Redis 优势

1. 性能极高 – Redis能读的速度是110000次/s,写的速度是81000次/s 。
2. 丰富的数据类型 – Redis支持二进制案例的 Strings, Lists, Hashes, Sets 及 Ordered Sets 数据类型操作。
3. 原子 – Redis的所有操作都是原子性的，意思就是要么成功执行要么失败完全不执行。单个操作是原子性的。多个操作也支持事务，即原子性，通过 MULTI 和 EXEC 指令包起来。
4. 丰富的特性 – Redis还支持 publish/subscribe, 通知, key 过期等等特性

## 安装

### Linux下安装Redis

1. 下载文件  wget http://download.redis.io/releases/redis-4.0.11.tar.gz 

2. 压缩文件  tar -zxvf redis-4.0.11.tar.gz

3. cd redis-4.0.11

4. make 

5. sudo make install  (默认安装在 /usr/local/redis,或指定PREFIX=)

6. mv redis.conf /usr/local/redis/etc (没有则创建etc)

7. vi /usr/local/redis/etc/redis.conf  (daemonize no为yes 后台启动)

8. /usr/local/redis/bin/redis-server /usr/local/redis/etc/redis.conf (开启redis )

9. 设置开机启动 vi /etc/rc.local (添加命令8)

#### 停止删除Redis

```text
pkill redis 停止
rm -rf /usr/local/redis 删除
```

### docker 安装 Redis
    
1. docker pull redis:4.0
    
2. docker run --name redis4 -p 6379:6379 -v $PWD/data:/data  -d redis:4.0 redis-server --appendonly yes
    
命令说明：
  
    -p 6379:6379 : 将容器的6379端口映射到主机的6379端口
    
    -v $PWD/data:/data : 将主机中当前目录下的data挂载到容器的/data
    
    redis-server --appendonly yes : 在容器执行redis-server启动命令，并打开redis持久化配置

### Redis配置

> Redis 的配置文件位于 Redis 安装目录下，文件名为 redis.conf (Windows 名为 redis.windows.conf)。

#### 通过 CONFIG 命令查看或设置配置项。

语法

```shell script
# CONFIG GET CONFIG_SETTING_NAME
CONFIG GET loglevel
CONFIG GET *  # 使用 * 号获取所有配置项：
```

#### 通过 CONFIG SET 命令修改配置
> 也可以通过修改 redis.conf 文件

```shell script
# CONFIG SET CONFIG_SETTING_NAME NEW_CONFIG_VALUE
CONFIG SET loglevel "notice"
CONFIG GET loglevel
```
配置项说明如下：

|配置项	| 说明|
|:---- |:---- |
| daemonize no | Redis 默认不是以守护进程的方式运行，可以通过该配置项修改，使用 yes 启用守护进程（Windows 不支持守护线程的配置为 no ）|
| pidfile /var/run/redis.pid	| 当 Redis 以守护进程方式运行时，Redis 默认会把 pid 写入 /var/run/redis.pid 文件，可以通过 pidfile 指定|
| port 6379	| 指定 Redis 监听端口，默认端口为 6379，作者在自己的一篇博文中解释了为什么选用 6379 作为默认端口，因为 6379 在手机按键上 MERZ 对应的号码，而 MERZ 取自意大利歌女 Alessia Merz 的名字
| bind 127.0.0.1	| 绑定的主机地址
| timeout 300	| 当客户端闲置多长秒后关闭连接，如果指定为 0 ，表示关闭该功能
| loglevel notice	| 指定日志记录级别，Redis 总共支持四个级别：debug、verbose、notice、warning，默认为 notice
| logfile stdout	| 日志记录方式，默认为标准输出，如果配置 Redis 为守护进程方式运行，而这里又配置为日志记录方式为标准输出，则日志将会发送给 /dev/null
| databases 16	| 设置数据库的数量，默认数据库为0，可以使用SELECT 命令在连接上指定数据库id
| save <seconds> <changes> | 在多长时间内，有多少次更新操作，就将数据同步到数据文件，可以多个条件配合 Redis 默认配置文件中提供了三个条件： `save 900 1` 表示 900 秒（15 分钟）内有 1 个更改 `save 300 10` 300 秒（5 分钟）内有 10 个更改 `save 60 10000`60 秒内有 10000 个更改	| 
| rdbcompression yes	| 指定存储至本地数据库时是否压缩数据，默认为 yes，Redis 采用 LZF 压缩，如果为了节省 CPU 时间，可以关闭该选项，但会导致数据库文件变的巨大
| dbfilename dump.rdb| 	指定本地数据库文件名，默认值为 dump.rdb
| dir ./	| 指定本地数据库存放目录
| slaveof <masterip> <masterport>| 设置当本机为 slave 服务时，设置 master 服务的 IP 地址及端口，在 Redis 启动时，它会自动从 master 进行数据同步
| masterauth <master-password>| 当 master 服务设置了密码保护时，slav 服务连接 master 的密码
| requirepass foobared| 设置 Redis 连接密码，如果配置了连接密码，客户端在连接 Redis 时需要通过 AUTH <password> 命令提供密码，默认关闭
| maxclients 128 | 设置同一时间最大客户端连接数，默认无限制，Redis 可以同时打开的客户端连接数为 Redis 进程可以打开的最大文件描述符数，如果设置 maxclients 0，表示不作限制。当客户端连接数到达限制时，Redis 会关闭新的连接并向客户端返回 max number of clients reached 错误信息
| maxmemory <bytes>| 指定 Redis 最大内存限制，Redis 在启动时会把数据加载到内存中，达到最大内存后，Redis 会先尝试清除已到期或即将到期的 Key，当此方法处理 后，仍然到达最大内存设置，将无法再进行写入操作，但仍然可以进行读取操作。Redis 新的 vm 机制，会把 Key 存放内存，Value 会存放在 swap 区
| appendonly no| 指定是否在每次更新操作后进行日志记录，Redis 在默认情况下是异步的把数据写入磁盘，如果不开启，可能会在断电时导致一段时间内的数据丢失。因为 redis 本身同步数据文件是按上面 save 条件来同步的，所以有的数据会在一段时间内只存在于内存中。默认为 no
| appendfilename appendonly.aof| 指定更新日志文件名，默认为 appendonly.aof
| appendfsync everysec	|  指定更新日志条件，共有 3 个可选值：no：表示等操作系统进行数据缓存同步到磁盘（快）always：表示每次更新操作后手动调用 fsync() 将数据写到磁盘（慢，安全）everysec：表示每秒同步一次（折中，默认值）
| vm-enabled no	| 指定是否启用虚拟内存机制，默认值为 no，简单的介绍一下，VM 机制将数据分页存放，由 Redis 将访问量较少的页即冷数据 swap 到磁盘上，访问多的页面由磁盘自动换出到内存中（在后面的文章我会仔细分析 Redis 的 VM 机制）
| vm-swap-file /tmp/redis.swap	| 虚拟内存文件路径，默认值为 /tmp/redis.swap，不可多个 Redis 实例共享
| vm-max-memory 0	| 将所有大于 vm-max-memory 的数据存入虚拟内存，无论 vm-max-memory 设置多小，所有索引数据都是内存存储的(Redis 的索引数据 就是 keys)，也就是说，当 vm-max-memory 设置为 0 的时候，其实是所有 value 都存在于磁盘。默认值为 0
| vm-page-size 32	| Redis swap 文件分成了很多的 page，一个对象可以保存在多个 page 上面，但一个 page 上不能被多个对象共享，vm-page-size 是要根据存储的 数据大小来设定的，作者建议如果存储很多小对象，page 大小最好设置为 32 或者 64bytes；如果存储很大大对象，则可以使用更大的 page，如果不确定，就使用默认值
| vm-pages 134217728	| 设置 swap 文件中的 page 数量，由于页表（一种表示页面空闲或使用的 bitmap）是在放在内存中的，，在磁盘上每 8 个 pages 将消耗 1byte 的内存。
| vm-max-threads 4	| 设置访问swap文件的线程数,最好不要超过机器的核数,如果设置为0,那么所有对swap文件的操作都是串行的，可能会造成比较长时间的延迟。默认值为4
| glueoutputbuf yes	| 设置在向客户端应答时，是否把较小的包合并为一个包发送，默认为开启
| hash-max-zipmap-entries 64 `hash-max-zipmap-value 512` | 指定在超过一定的数量或者最大的元素超过某一临界值时，采用一种特殊的哈希算法
| activerehashing yes	| 指定是否激活重置哈希，默认为开启（后面在介绍 Redis 的哈希算法时具体介绍）
| include /path/to/local.conf	| 指定包含其它的配置文件，可以在同一主机上多个Redis实例之间使用同一份配置文件，而同时各个实例又拥有自己的特定配置文件

### Redis 连接

1. `AUTH password` 验证密码是否正确
2. `ECHO message ` 打印字符串
3. `PING `  查看服务是否运行
4. `QUIT`  关闭当前连接
5. `SELECT index` 切换到指定的数据库

### Redis 服务器命令

1. `BGREWRITEAOF
`  异步执行一个 AOF（AppendOnly File） 文件重写操作
2. `BGSAVE
`  在后台异步保存当前数据库的数据到磁盘
3. `CLIENT KILL [ip:port] [ID client-id]
`  关闭客户端连接
4. `CLIENT LIST
`  获取连接到服务器的客户端连接列表
5. `CLIENT GETNAME
`  获取连接的名称
6. `CLIENT PAUSE timeout
`  在指定时间内终止运行来自客户端的命令
7. `CLIENT SETNAME connection-name
`  设置当前连接的名称
8. `CLUSTER SLOTS
`  获取集群节点的映射数组
9. `COMMAND
`  获取 Redis 命令详情数组
10. `COMMAND COUNT
`  获取 Redis 命令总数
11. `COMMAND GETKEYS
`  获取给定命令的所有键
12. `TIME
`  返回当前服务器时间
13. `COMMAND INFO command-name [command-name ...]
`  获取指定 Redis 命令描述的数组
14. `CONFIG GET parameter
`  获取指定配置参数的值
15. `CONFIG REWRITE
`  对启动 Redis 服务器时所指定的 redis.conf 配置文件进行改写
16. `CONFIG SET parameter value
`  修改 redis 配置参数，无需重启
17. `CONFIG RESETSTAT
`  重置 INFO 命令中的某些统计数据
18. `DBSIZE
`  返回当前数据库的 key 的数量
19. `DEBUG OBJECT key
`  获取 key 的调试信息
20. `DEBUG SEGFAULT
`  让 Redis 服务崩溃
21. `FLUSHALL
`  删除所有数据库的所有key
22. `FLUSHDB
`  删除当前数据库的所有key
23. `INFO [section]
`  获取 Redis 服务器的各种信息和统计数值
24. `LASTSAVE
`  返回最近一次 Redis 成功将数据保存到磁盘上的时间，以 UNIX 时间戳格式表示
25. `MONITOR
`  实时打印出 Redis 服务器接收到的命令，调试用
26. `ROLE
`  返回主从实例所属的角色
27. `SAVE
`  同步保存数据到硬盘
28. `SHUTDOWN [NOSAVE] [SAVE]
`  异步保存数据到硬盘，并关闭服务器
29. `SLAVEOF host port
`  将当前服务器转变为指定服务器的从属服务器(slave server)
30. `SLOWLOG subcommand [argument]
`  管理 redis 的慢日志
31. `SYNC
`  用于复制功能(replication)的内部命令

### Redis 数据备份与恢复

1. `SAVE` 创建当前数据库的备份
2. ` BGSAVE ` 创建 redis 备份文件

如果需要恢复数据，只需将备份文件 (dump.rdb) 移动到 redis 安装目录并启动服务即可。
获取 redis 目录可以使用 CONFIG 命令，` CONFIG GET dir `

### Redis 安全
1. `CONFIG get requirepass ` 查看是否设置了密码验证 
2. `CONFIG set requirepass "123456" `  设置密码验证 

### Redis 性能测试

基本命令如下： `redis-benchmark [option] [option value]`
> 注意：该命令是在 redis 的目录下执行的，而不是 redis 客户端的内部指令。
    
redis 性能测试工具可选参数如下所示：
    
    序号	选项	描述	默认值
    1	-h	指定服务器主机名	127.0.0.1
    2	-p	指定服务器端口	6379
    3	-s	指定服务器 socket	
    4	-c	指定并发连接数	50
    5	-n	指定请求数	10000
    6	-d	以字节的形式指定 SET/GET 值的数据大小	2
    7	-k	1=keep alive 0=reconnect	1
    8	-r	SET/GET/INCR 使用随机 key, SADD 使用随机值	
    9	-P	通过管道传输 <numreq> 请求	1
    10	-q	强制退出 redis。仅显示 query/sec 值	
    11	--csv	以 CSV 格式输出	
    12	-l	生成循环，永久执行测试	
    13	-t	仅运行以逗号分隔的测试命令列表。	
    14	-I	Idle 模式。仅打开 N 个 idle 连接并等待。	
    
redis-benchmark -h 127.0.0.1 -p 6379 -t set,lpush -n 10000 -q

以上实例中主机为 127.0.0.1，端口号为 6379，执行的命令为 set,lpush，请求数为 10000，通过 -q 参数让结果只显示每秒执行的请求数。

### Redis 管道技术
> Redis是一种基于客户端-服务端模型以及请求/响应协议的TCP服务。这意味着通常情况下一个请求会遵循以下步骤：
    
1. 客户端向服务端发送一个查询请求，并监听Socket返回，通常是以阻塞模式，等待服务端响应。
2. 服务端处理命令，并将结果返回给客户端。

Redis 管道技术可以在服务端未响应时，客户端可以继续向服务端发送请求，并最终一次性读取所有服务端的响应

### Redis 分区
> 分区是分割数据到多个Redis实例的处理过程，因此每个实例只保存key的一个子集。

#### 分区的优势
 * 通过利用多台计算机内存的和值，允许我们构造更大的数据库。
 * 通过多核和多台计算机，允许我们扩展计算能力；通过多台计算机和网络适配器，允许我们扩展网络带宽。
#### 分区的不足
redis的一些特性在分区方面表现的不是很好：

 * 涉及多个key的操作通常是不被支持的。举例来说，当两个set映射到不同的redis实例上时，你就不能对这两个set执行交集操作。
 * 涉及多个key的redis事务不能使用。
 * 当使用分区时，数据处理较为复杂，比如你需要处理多个rdb/aof文件，并且从多个实例和主机备份持久化文件。
 * 增加或删除容量也比较复杂。redis集群大多数支持在运行时增加、删除节点的透明数据平衡的能力，但是类似于客户端分区、代理等其他系统则不支持这项特性。然而，一种叫做presharding的技术对此是有帮助的。
#### 分区类型
Redis 有两种类型分区。 
假设有4个Redis实例 R0，R1，R2，R3，和类似user:1，user:2这样的表示用户的多个key，对既定的key有多种不同方式来选择这个key存放在哪个实例中。
也就是说，有不同的系统来映射某个key到某个Redis服务。

##### 范围分区
最简单的分区方式是按范围分区，就是映射一定范围的对象到特定的Redis实例。

比如，ID从0到10000的用户会保存到实例R0，ID从10001到 20000的用户会保存到R1，以此类推。

并且在实际中使用，不足就是要有一个区间范围到实例的映射表。
这个表要被管理，同时还需要各 种对象的映射表，通常对Redis来说并非是好的方法。

##### 哈希分区
对任何key都适用，也无需是object_name:这种形式，像下面描述的一样简单：

 * 用一个hash函数将key转换为一个数字，比如使用crc32 hash函数。对key foobar执行crc32(foobar)会输出类似93024922的整数。
 * 对这个整数取模，将其转化为0-3之间的数字，就可以将这个整数映射到4个Redis实例中的一个了。93024922 % 4 = 2，就是说key foobar应该被存到R2实例中。注意：取模操作是取除的余数，通常在多种编程语言中用%操作符实现。
