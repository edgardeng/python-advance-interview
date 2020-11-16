# Redis Stream

> Redis 5.0 全新的数据类型：streams，以更抽象的方式建模日志的数据结构。
> Redis的streams主要是一个append only的数据结构，至少在概念上它是一种在内存中表示的抽象数据类型，只不过它们实现了更强大的操作，以克服日志文件本身的限制。
 
Redis Stream 主要用于消息队列（MQ，Message Queue）

* Redis本身的发布订阅 (pub/sub) 可以分发消息，但无法记录历史消息。（网络断开、Redis 宕机等，消息就会被丢弃）

* Redis Stream 提供了消息的持久化和主备复制功能, 允许消费者等待生产者加入到streams的新数据

## Stream 数据结构
![](./redis_stream.png)


每个 Stream 都有唯一的名称，它就是 Redis 的 key，在我们首次使用 xadd 指令追加消息时自动创建。

 * Consumer Group ：消费组，使用 XGROUP CREATE 命令创建，一个消费组有多个消费者(Consumer)。
 * last_delivered_id ：游标，每个消费组会有个游标 last_delivered_id，任意一个消费者读取了消息都会使游标 last_delivered_id 往前移动。
 * pending_ids ：消费者(Consumer)的状态变量，作用是维护消费者的未确认的 id。 pending_ids 记录了当前已经被客户端读取的消息，但是还没有 ack (Acknowledge character：确认字符）。
 
redis源码中,定义streams结构的源码如下，stream的核心数据结构是radix tree：

```c
typedef struct stream {
 
    rax *rax;               /* The radix tree holding the stream. */
 
    uint64_t length;        /* Number of elements inside this stream. */
 
    streamID last_id;       /* Zero if there are yet no items. */
 
    rax *cgroups;           /* Consumer groups dictionary: name -> streamCG */
 
} stream;
```

[源码参考]()https://github.com/antirez/redis/blob/5.0.0/src/stream.h)


## 相关命令 

### 消息队列相关命令
 * `XADD key ID field value [field value ...]` - 添加消息到末尾
   * ID ：消息id，使用 * 表示由 redis 默认生成（ID格式为millisecondsTime+sequenceNumber，即当前毫秒级别的时间戳加上一个自增序号值），可以自定义，但是要自己保证递增性
    * field value ： 记录
 * XTRIM - 对流进行修剪，限制长度 `XTRIM key MAXLEN [~] count`
 * `XDEL key ID [ID …]` - 删除消息
 * XLEN - 获取流包含的元素数量，即消息长度
 * `XRANGE key start end [COUNT count]` - 获取消息列表，会自动过滤已经删除的消息
 * `XREVRANGE key end start [COUNT count]` - 反向获取消息列表，ID 从大到小
 * XREAD - 以阻塞或非阻塞方式获取消息列表
 
### 消费者组相关命令：

 * XGROUP CREATE - 创建消费者组
 * XREADGROUP GROUP - 读取消费者组中的消息
 * ` XACK key group ID [ID …] ` - 将消息标记为"已处理"
 * XGROUP SETID - 为消费者组设置新的最后递送消息ID
 * XGROUP DELCONSUMER - 删除消费者
 * XGROUP DESTROY - 删除消费者组
 * `XPENDING key group [start end count] [consumer]` - 显示待处理消息的相关信息
 * XCLAIM - 转移消息的归属权 `XCLAIM key group consumer min-idle-time ID [ID …] [IDLE ms] [TIME ms-unix-time] [RETRYCOUNT count] [FORCE] [JUSTID]`
 * XINFO - 查看流和消费者组的相关信息；
 * XINFO GROUPS - 打印消费者组的信息；
 * XINFO STREAM - 打印流信息


Stream 三种查询模式
 
* 范围查询：因为streams的每个entry，其默认生成的ID是基于时间且递增的
  ```shell script
  XRANGE userInfo "1540014096298-0" "1540014477236-0" # 某个顺序范围下的元素，start参数是更小的ID，end参数是更大的ID
  XRANGE mystream - + # 符号"-"表示最小的ID，符号"+"表示最大的ID
  XRANGE userInfo 1540014496505-1  1540051199000-0 COUNT 5
  XREVRANGE userInfo "1540014477236-0" "1540014096298-0"
  ```
 
* 监听模式：类比linux中的tailf命令，实时接收新增加到streams中的entry（也有点像一个消息系统，事实上笔者认为它就是借鉴了kafka）
  ```shell script
  XREAD COUNT 10 BLOCK 60000 STREAMS userInfo "1540041139268-0" # 返回streams中从来没有读取的，且比参数ID更大的元素。
  XREAD COUNT 2 STREAMS userInfo 0
  XREAD BLOCK 0 STREAMS userInfo $ #  说明BLOCK为0表示一致等待知道有新的数据，否则永远不会超时, 特殊字符`$`表示，只获取最新添加的消息
  XREAD BLOCK 0 STREAMS userInfo_01 userInfo_02 userInfo_03 userInfo_04  $ $ $ $ # XREAD还支持同时监听多个streams， # 监听userInfo_01~userInfo_04这4个streams的新的消息。
  ```

* 消费者组：即Consumer Groups，特殊的监听模式。从一个消费者的角度来看streams，一个streams能被分区到多个处理消息的消费者，对于任意一条消息，同一个消费者组中只有一个消费者可以处理（和kafka的消费者组完全一样）。这样还能够横向扩容消费者，从而提升处理消息的能力，而不需要只让把让一个消费者处理所有消息

  ```shell script
  XGROUP CREATE userInfo GRP-AFEI $  # 创建一个消费者组 (目前XGROUP CREATE的streams必须是一个存在的streams，否则会报错)
  XREADGROUP GROUP mygroup zhangsan COUNT 1 BLOCK 0 STREAMS userInfo >  # 名为zhangsan的消费者，需要注意的是streams名称userInfo后面的特殊符号`>`表示这个消费者只接收从来没有被投递给其他消费者的消息，即新的消息
  XREADGROUP GROUP mygroup lisi COUNT 1 BLOCK 0 STREAMS userInfo >      # 名为lisi的消费者
  XADD userInfo * username u102102 password p102102                     # 添加两条信息
  XADD userInfo * username u102103 password p102103
  XREADGROUP GROUP mygroup lisi COUNT 5 BLOCK 0 STREAMS userInfo 0      # 消费者lisi有一条消息
  XACK userInfo mygroup 1540081890919-0                                 # 通过命令ack这条消息
  XREADGROUP GROUP mygroup lisi COUNT 5 BLOCK 0 STREAMS userInfo 0      # 再看消费者lisi的pending队列，已经为空
  
  XPENDING userInfo mygroup - + 10                                      # 查看消费者组下总计最多10条pending消息
  XPENDING userInfo mygroup - + 10 zhangsan                             # 查看消费者组下zhangsan这个消费者总计最多10条pending消息
  XREADGROUP GROUP mygroup zhangsan COUNT 5 BLOCK 0 STREAMS userInfo 0  # 改变消费者组中消息的所有权
  XCLAIM userInfo mygroup zhangsan 360 1540083266293-0                  # zhangsan本来有1条消息，现在将另一条本来属于lisi的消息的所有权转给它：
  XREADGROUP GROUP mygroup zhangsan COUNT 5 BLOCK 0 STREAMS userInfo 0  # 现在zhangsan有两条消息了
  XINFO CONSUMERS userInfo mygroup                                      # 得到streams和消费者组的一些信息 
  XINFO STREAM userInfo 
  XTRIM userInfo MAXLEN 10                    # streams只保留10条消息，其返回结果表示被剪去多少条消息：
  ```
  
  假设有三个消费者C1，C2，C3。在streams中总计有7条消息：1， 2， 3， 4， 5， 6， 7，那么消费关系如下所示：
  ```
    1 -> C1   
    2 -> C2   
    3 -> C3
    4 -> C1
    5 -> C2
    6 -> C3
    7 -> C1
  ```

  消费者组具备如下几个特点：
    1. 同一个消息不会被投递到一个消费者组下的多个消费者，只可能是一个消费者。
    2. 同一个消费者组下，每个消费者都是唯一的，通过大小写敏感的名字区分。
    3. 消费者组中的消费者请求的消息，一定是新的，从来没有投递过的消息。
    4. 消费一个消息后，需要用命令（XACK）确认，意思是说：这条消息已经给成功处理。正因为如此，当访问streams的历史消息时，每个消费者只能看到投递给它自己的消息。
 
## 持久化，复制以及消息安全性
 
1. STREAM会异步复制到slave，并也会持久化到AOF和RDB文件中。
   然而，消费者组的全部状态是被传播（propagated ）到AOF，RDB和slave中。
 
> 需要注意的是，Redis的streams和消费者组使用Redis默认复制进行持久化和复制，因此：如果消息的持久性在您的应用程序中很重要，则必须将AOF与强fsync策略一起使用。
 
2. 默认情况下，异步复制不保证能复制每一个数据添加或使用者组状态更改：在故障转移之后，可能会丢失某些内容，具体取决于slave从master接收数据的能力。
3. 其他数据类型，例如Lists，Sets等，如果所有元素都被删除，那么key也不存在。而streams允许所有entry都被删除, 存在长度为0的streams
    > 因为STREAM可能具有关联的消费者组，并且我们不希望由于STREAM不再有任何entry而丢失消费者组定义的状态。 目前，即使没有关联的消费者群体，也不会删除该STREAM

## 消息如果忘记ACK会怎样
 Stream在每个消费者结构中保存了正在处理中的消息ID列表PEL，如果消费者收到了消息处理完了但是没有回复ack，就会导致PEL列表不断增长，
 如果有很多消费组的话，那么这个PEL占用的内存就会放大。

## PEL如何避免消息丢失
在客户端消费者读取Stream消息时，Redis服务器将消息回复给客户端的过程中，客户端突然断开了连接，消息就丢失了。
但是PEL里已经保存了发出去的消息ID。待客户端重新连上之后，可以再次收到PEL中的消息ID列表。
不过此时xreadgroup的起始消息ID不能为参数>，而必须是任意有效的消息ID，一般将参数设为0-0，表示读取所有的PEL消息以及自last_delivered_id之后的新消息
