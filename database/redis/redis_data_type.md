# Redis

> Redis是一个开源的使用ANSIC语言编写、支持网络、可基于内存亦可持久化的日志型、Key-Value数据库，并提供多种语言的API。

Redis支持存储的value类型相对更多，包括string(字符串)、list(链表)、set(集合)、zset(sorted set --有序集合)和hash（哈希类型）。

这些数据类型都支持push/pop、add/remove及取交集并集和差集及更丰富的操作，而且这些操作都是原子性的。

redis支持各种不同方式的排序。与memcached一样，为了保证效率，数据都是缓存在内存中。

区别的是redis会周期性的把更新的数据写入磁盘或者把修改操作写入追加的记录文件，并且在此基础上实现了master-slave(主从)同步。


## Redis的使用

### Redis命令

Redis 客户端的基本语法: `$ redis-cli`

* 远程登录 `$ redis-cli -h host -p port -a password`

Redis 键命令的基本语法如下： `COMMAND KEY_NAME` 

* 设置健值 `SET key_name redis`
* 获取指定key的值  `GET key_name`
* 删除健值 `DEL key_name`
* 被序列化的值 `DUMP key_name`
* 检查健值存在 `EXISTS key_name`
* 设置过期时间,单位以秒计  `EXPIRE key_name 60`
* UNIX时间戳,设置过期时间 `EXPIREAT key_name 1293840000`
* 设置过期时间,单位以毫秒计 `PEXPIRE key_name 1500`
* 移除key的过期时间，持久保持。 `PERSIST key_name`
* key的剩余的过期时间(毫秒)   `PTTL key_name`
* key的剩余的过期时间(秒)   `TTL key_name`
* 储存的值的类型 `TYPE key`

* 获取所有的key `KEYS *`
* 查找所有符合给定模式的key  `KEYS key_*`
* 服务器的统计信息 `INFO`

### Redis在Python中的使用

1. install `pip install redis`

2. base usage

```python
from redis import Redis
redis = Redis(host='localhost', port=6379, db=0)
redis.set('openCount', 0)
redis.incr('openCount')
redis.get('openCount')

# pipline的使用
pipe = redis.pipeline()
pipe.set('foo', 'bar')
pipe.expireat('foo',111111)
pipe.execute()
```

3. [more api](http://redisdoc.com/)

* keys      所有的key
* dbsize    数据库几条数据
* delete('key')
* save      
* flushdb() 清空数据库
* hset('key','hash_key','hash_value') 添加hash值
* hincrby('key','hash_key', 1) 自增hash值
* hgetall('key') 获取hash值
* hkeys('key') 获取hash值的key

### Redis中的5种数据结构与常用场景

#### 1. String 字符串

|常用操作|说明|
|:----|:----|
|SET key value  |   存入字符串|
|MSET key value [k v ...] |   批量存入存入字符串|
|SETNX key value  |   存入一个不存在的字符串（set if not exists）|
|GET key  |   通过键获取一个字符串|  
|MGET key [k ...]  |   通过多个键批量获取字符串|
|DEL key [k ...] |   删除一个或多个|
|EXPIRE key seconds |   设置过期时间|
|INCR key  |   将KEY中存储的数值 +1 |
|DECR key  |   将KEY中存储的数值 -1 |
|INCRBY key increment |   将KEY中存储的数值 +increment |
|DECRBY key decrement |   将KEY中存储的数值 -decrement |


应用场景：

 * 计数器
    `INCR article:read_count:{id} ` 将某个文章的阅读量+1
 * Web集群的Session共享
 
 * 分布式系统全局序列号
    `INCRBY order_id 1000 `  使用redis批量生成序列号提高性能   

#### 2. Hash 哈希对

|常用操作|说明|
|:----|:----|
|HSET key field value           |   存入一个哈希表的健值对|
|HMSET key field value [f v ...]|   在一个哈希表批量存入健值对|
|HSETNX key field value         |   存入一个key不存在的哈希表的健值对（set if not exists）|
|HGET key field                 |   通过key获取哈希表对应field的值|  
|HMGET key field [f ...]        |   通过key获取哈希表对应多个field的值|
|HDEL key field [f ...]         |   删除一个或多个field|
|HLEN key  |   获取哈希表中filed的数量 |
|HGETALL key  |    通过key获取哈希表所有的键值对 |
|HINCRBY key field increment |   通过key获取哈希表 将对应field的数值 +increment |

应用场景：

 * 对象缓存
    `HMSET user {user_id}:name Jack {user_id}:age 10 ` 添加一个用户
    `HMSET user 2:name Mck 2:age 12 ` 添加一个用户
 
 * 电商购物车
    > 用户ID为key，商品id为field，数量为value   
    * `HSET cart:1 1000 1` 添加商品
    * `HINCRBY cart:1 1000 1` 添加商品数量
    * `HLEN cart:1 `    商品总数
    * `HDEL cart:1 1000 ` 删除某个商品
    * `HGETALL cart:1 `     获取所有的商品

优点：
  * 同类数据归类整合存储，方便数据管理
  * 相比string操作内存消耗与CPU更少
  * 比String 更节省空间
  
缺点：
 * 过去功能不能用在field上
 * Redis集群架构上不适合大规模使用   
    
#### 3. List 列表

|常用操作|说明|
|:----|:----|
|LPUSH key value [v ...]        |   将多个值 插入key列表的表头|
|RPUSH key  value [v ...]       |   将多个值 插入key列表的表尾|
|LPOP key                       |   移除并返回key列表的头元素|
|RPOP key                       |   移除并返回key列表的尾元素|  
|LRANGE key start stop          |   返回制定区间的元素 双闭合区间|
|BLPOP key [k ...] timeout      |  从key列表表头弹出一个元素， 若没有则阻塞等待timeout秒，若timeout=0，一直阻塞|
|BRPOP key [k ...] timeout      |  从key列表末尾弹出一个元素， 若没有则阻塞等待timeout秒，若timeout=0，一直阻塞|

应用场景：

 * 常用数据结构
    * Stack 栈 = LPUSH +  LPOP -》 FILO
    * Queue 队列 = LPUSH + RPOP
    * Block MQ = LPUSH + BRPOP 

 * 微博/微信 消息流
    > A 关注了B，C
    * `LPUSH user:a 10001` 用户A发了微博消息10001
    * `LPUSH user:a 10002` 用户B发了微博消息10002 
    * `LRANGE user:a 0 4` 用户A查看最新消息

#### 4. Set 集合

|常用操作|说明|
|:----|:----|
|SADD key member [m ...]        |   往集合key中，添加元素（若存在，则忽略）|
|SREM key  value [v ...]       |   从集合key中，删除元素|
|SMEMBERS key |   从集合key中，获取所有元素|
|SCARD key |   获取集合key中，元素个数|
|SISMENMBER key member|   集合key中，是否存在元素member|
|SRANDMEMBER key [count]|   从集合key中，随机选出count个元素， 不删除|
|SPOP key [count]|   从集合key中，随机选出count个元素， 并删除|
|SINTER key [key ...]                      |   求交集|
|SINTERSTORE destination key [key ...]     |   求交集， 结果存入新集合destination|  
|SUNION key [key ...]                      |   求并集|
|SUNIONSTORE destination key [key ...]     |   求并集， 结果存入新集合destination|  
|SDIFF key [key ...]                      |   求差集 第1个减去后面所有的|
|SDIFFSTORE destination key [key ...]     |   求差集， 结果存入新集合destination|  

应用场景：
 * 随机抽奖
    * `SADD key {user_id} ` 添加抽奖用户
    * `SMEMBERS key  ` 所有的抽奖用户
    * `SRANDMEMBER key 10 / SPOP key 10` 抽取10个中奖用户
 * 点赞，收藏，标签
    * `SADD like:1 {user_id}`   点赞
    * `SREM like:1 {user_id}`   取消点赞
    * `SCARD like:1  `          点赞数
 * 微博关注模型
    * A关注的人： aSet -> {b,c,d}
    * B关注的人： bSet -> {a,e,d, f}
    * C关注的人： cSet -> {b, d, f, g}
    * A和B共同关注的人: SINET aSet bSet -> { d }
    * 我关注的人也关注了TA
    * 我可能认识的人： SDIFF aSet bSet cSet
 * 电商商品的筛选 （交集）
    
#### 5. ZSet 有序集合

|常用操作|说明|
|:----|:----|
|ZADD key score member [score member ...] |   往集合key中，添加带分值的元素|
|ZREM key  member [member ...]       |   从集合key中，删除元素|
|ZSCORE key member                   |   获取集合key中，某个元素的分值|
|ZINCRBY key increment member        |   集合key中，某个元素的分值 + increment|
|ZCARD key                           |   获取集合key中，元素个数|
|ZRANGE key start stop [withscores]|   集合key中，从start到stop下标的元素  成员的位置按分数值递减(从小到大)来排列。|
|ZREVRANGE key start stop [withscores]|   倒叙获取集合key中，从start到stop下标的元素 成员的位置按分数值递减(从大到小)来排列|
|ZINTERZTORE deZtination numkeys key [key ...]     |   求交集， 结果存入新集合deZtination|  
|ZUNIONZTORE deZtination numkeys key [key ...]     |   求并集， 结果存入新集合deZtination|   


应用场景：
 * 热搜排行榜
    * `ZINCRBY hot_news:20200101 1 topc_a`  给20200101的新闻topc_a 添加热度
    * `ZREVRANGE hot_news:20200101 0 9 WITHSCORES` 当天20200101排前十的新闻
    * `ZUNIONZTORE hot_news:20200101-0107 7 hot_news:20200101 hot_news:20200102 ... hot_news:20200107` 7天的合集
    * `ZREVRANGE hot_news:20200101-0107  0 9 WITHSCORES` 七日内排前十的新闻

#### Redis更多使用场景

* 附近的人
* 摇一摇/抢红包
* 附近的车
* 自动补全
* 布隆过滤器

#### BitMap
##### 1、BitMap 是什么?

  通过一个bit位来表示某个元素对应的值或者状态,其中的key就是对应元素本身。
  我们知道8个bit可以组成一个Byte，所以bitmap本身会极大的节省储存空间。

##### 2、Redis中的BitMap

  Redis从2.2.0版本开始新增了setbit,getbit,bitcount等几个bitmap相关命令。
  虽然是新命令，但是并没有新增新的数据类型，因为setbit等命令只不过是在set上的扩展。

##### 3、 命令介绍
   * `SETBIT key offset value`  设置或者清空key的value(字符串)在offset处的bit值(只能只0或者1)。
 
##### 4、空间占用、以及第一次分配空间需要的时间

offset为2^32-1（分配512MB）需要～300ms，
offset为2^30-1(分配128MB)需要～80ms，
offset为2^28-1（分配32MB）需要～30ms，
offset为2^26-1（分配8MB）需要8ms。<来自官方文档>

大概的空间占用计算公式是：($offset/8/1024/1024)MB

##### 5、使用场景

 1. 用户签到

根据日期 offset =hash % 365  ； key = 年份#用户id
```shell script
setbit 2018#user1 1 1
setbit 2018#user1 2 1
bitcount 2018#user1
```
> 签到功能(这里不考虑数据落地事宜)，并且需要展示最近一个月的签到情况
 
 2. 统计活跃用户
使用时间作为cacheKey，然后用户ID为offset，如果当日活跃过就设置为1

如果计算某几天/月/年的活跃用户呢(暂且约定，统计时间内只有有一天在线就称为活跃)，有请下一个redis的命令
命令 BITOP operation destkey key [key ...]
说明：对一个或多个保存二进制位的字符串 key 进行位元操作，并将结果保存到 destkey 上。
说明：BITOP 命令支持 AND 、 OR 、 NOT 、 XOR 这四种操作中的任意一种参数

```shell script
setbit 20200101 1 1
setbit 20200101 2 1
setbit 20200102 1 1
bitop and result1 20200101 20200102
bitcount result1 # 1

bitop or result2 20200101 20200102
bitcount result2 # 2
```

 3. 用户在线状态
 
    使用bitmap是一个节约空间效率又高的一种方法，只需要一个key，然后用户ID为offset，如果在线就设置为1，
    不在线就设置为0，和上面的场景一样，5000W用户只需要6MB的空间。
#### HyperLogLog
Redis HyperLogLog 是用来做基数统计的算法

1. HyperLogLog 的优点是，在输入元素的数量或者体积非常非常大时，计算基数所需的空间总是固定的、并且是很小的。

2. 在 Redis 里面，每个 HyperLogLog 键只需要花费 12 KB 内存，就可以计算接近 2^64 个不同元素的基 数。
  这和计算基数时，元素越多耗费内存就越多的集合形成鲜明对比。

但是，因为 HyperLogLog 只会根据输入元素来计算基数，而不会储存输入元素本身，所以 HyperLogLog 不能像集合那样，返回输入的各个元素。

##### 什么是基数?
比如数据集 {1, 3, 5, 7, 5, 7, 8}， 那么这个数据集的基数集为 {1, 3, 5 ,7, 8}, 基数(不重复元素)为5。 
基数估计就是在误差可接受的范围内，快速计算基数。

##### 命令介绍

* `pfadd key element [element...]` 将所有元素参数添加到 HyperLogLog 数据结构中,如果至少有个元素被添加返回 1， 否则返回 0

* `pfcount key [key...] ` 返回给定 HyperLogLog 的基数估算值。返回给定 HyperLogLog 的基数值，如果多个 HyperLogLog 则返回基数估值之和

* `pfmerge destkey sourcekey [sourcekey...] ` 将多个 HyperLogLog 合并为一个 HyperLogLog ，合并后的 HyperLogLog 的基数估算值是通过对所有 给定 HyperLogLog 进行并集计算得出的。

##### 案例

淘宝网店10个宝贝链接的独立访客（Unique Visitor，简称UV）数

 1. 对独立访客做标识

 2. 在访客点击链接时记录下链接编号及访客标记

 3. 对每一个要统计的链接维护一个数据结构和一个当前UV值，当某个链接发生一次点击时，能迅速定位此用户在今天是否已经点过此链接，如果没有则此链接的UV增加1

#### GEO

Redis GEO 主要用于存储地理位置信息，并对存储的信息进行操作，该功能在 Redis 3.2 版本新增。

Redis GEO 操作方法有：

 * `GEOADD key longitude latitude member [longitude latitude member ...]` ：添加地理位置的坐标。
 * `GEOPOS key member [member ...]` ：获取地理位置的坐标。
 * `GEODIST key member1 member2 [m|km|ft|mi]`：计算两个位置之间的距离 (m ：米，默认单位 km ：千米 mi ：英里 ft ：英尺 )
 * `GEORADIUS key longitude latitude radius m|km|ft|mi [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count] [ASC|DESC] [STORE key] [STOREDIST key]`：根据用户给定的经纬度坐标来获取指定范围内的地理位置集合
   * WITHDIST: 在返回位置元素的同时， 将位置元素与中心之间的距离也一并返回。
   * WITHCOORD: 将位置元素的经度和维度也一并返回。
   * WITHHASH: 以 52 位有符号整数的形式， 返回位置元素经过原始 geohash 编码的有序集合分值。 这个选项主要用于底层应用或者调试， 实际中的作用并不大。
   * COUNT 限定返回的记录数。
   * ASC: 查找结果根据距离从近到远排序。
   * DESC: 查找结果根据从远到近排序
 * `GEORADIUSBYMEMBER key member radius .. 同上`：根据储存在位置集合里面的某个地点获取指定范围内的地理位置集合。
 * `GEOHASH key member [member ...]`：返回一个或多个位置对象的 geohash 值
 
```shell script
GEOADD Sicily 13.361389 38.115556 "Palermo" 15.087269 37.502669 "Catania" 
GEODIST Sicily Palermo Catania # 默认 m
GEORADIUS Sicily 15 37 100 km
GEORADIUS Sicily 15 37 200 km

``` 

### 参考

[data-types-intro](https://redis.io/topics/data-types-intro)

[菜鸟教程-Redis 数据类型](https://www.runoob.com/redis/redis-data-types.html)
