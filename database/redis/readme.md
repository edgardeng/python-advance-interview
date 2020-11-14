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

```shell scriptf
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
| slaveof <masterip> <masterport>| 	设置当本机为 slave 服务时，设置 master 服务的 IP 地址及端口，在 Redis 启动时，它会自动从 master 进行数据同步
| masterauth <master-password>	当 master 服务设置了密码保护时，slav 服务连接 master 的密码
| requirepass foobared	设置 Redis 连接密码，如果配置了连接密码，客户端在连接 Redis 时需要通过 AUTH <password> 命令提供密码，默认关闭
| maxclients 128	设置同一时间最大客户端连接数，默认无限制，Redis 可以同时打开的客户端连接数为 Redis 进程可以打开的最大文件描述符数，如果设置 maxclients 0，表示不作限制。当客户端连接数到达限制时，Redis 会关闭新的连接并向客户端返回 max number of clients reached 错误信息
| maxmemory <bytes>	指定 Redis 最大内存限制，Redis 在启动时会把数据加载到内存中，达到最大内存后，Redis 会先尝试清除已到期或即将到期的 Key，当此方法处理 后，仍然到达最大内存设置，将无法再进行写入操作，但仍然可以进行读取操作。Redis 新的 vm 机制，会把 Key 存放内存，Value 会存放在 swap 区
| appendonly no	指定是否在每次更新操作后进行日志记录，Redis 在默认情况下是异步的把数据写入磁盘，如果不开启，可能会在断电时导致一段时间内的数据丢失。因为 redis 本身同步数据文件是按上面 save 条件来同步的，所以有的数据会在一段时间内只存在于内存中。默认为 no
| appendfilename appendonly.aof	指定更新日志文件名，默认为 appendonly.aof
| appendfsync everysec	
指定更新日志条件，共有 3 个可选值：

no：表示等操作系统进行数据缓存同步到磁盘（快）
always：表示每次更新操作后手动调用 fsync() 将数据写到磁盘（慢，安全）
everysec：表示每秒同步一次（折中，默认值）
| vm-enabled no	指定是否启用虚拟内存机制，默认值为 no，简单的介绍一下，VM 机制将数据分页存放，由 Redis 将访问量较少的页即冷数据 swap 到磁盘上，访问多的页面由磁盘自动换出到内存中（在后面的文章我会仔细分析 Redis 的 VM 机制）
| vm-swap-file /tmp/redis.swap	虚拟内存文件路径，默认值为 /tmp/redis.swap，不可多个 Redis 实例共享
| vm-max-memory 0	将所有大于 vm-max-memory 的数据存入虚拟内存，无论 vm-max-memory 设置多小，所有索引数据都是内存存储的(Redis 的索引数据 就是 keys)，也就是说，当 vm-max-memory 设置为 0 的时候，其实是所有 value 都存在于磁盘。默认值为 0
| vm-page-size 32	Redis swap 文件分成了很多的 page，一个对象可以保存在多个 page 上面，但一个 page 上不能被多个对象共享，vm-page-size 是要根据存储的 数据大小来设定的，作者建议如果存储很多小对象，page 大小最好设置为 32 或者 64bytes；如果存储很大大对象，则可以使用更大的 page，如果不确定，就使用默认值
| vm-pages 134217728	设置 swap 文件中的 page 数量，由于页表（一种表示页面空闲或使用的 bitmap）是在放在内存中的，，在磁盘上每 8 个 pages 将消耗 1byte 的内存。
| vm-max-threads 4	设置访问swap文件的线程数,最好不要超过机器的核数,如果设置为0,那么所有对swap文件的操作都是串行的，可能会造成比较长时间的延迟。默认值为4
| glueoutputbuf yes	设置在向客户端应答时，是否把较小的包合并为一个包发送，默认为开启
| hash-max-zipmap-entries 64 `hash-max-zipmap-value 512` | 指定在超过一定的数量或者最大的元素超过某一临界值时，采用一种特殊的哈希算法
| activerehashing yes	指定是否激活重置哈希，默认为开启（后面在介绍 Redis 的哈希算法时具体介绍）
| include /path/to/local.conf	指定包含其它的配置文件，可以在同一主机上多个Redis实例之间使用同一份配置文件，而同时各个实例又拥有自己的特定配置文件
