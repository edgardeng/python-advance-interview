# 使用Redis 实现限流
保护高并发系统的三大利器：缓存、降级和限流。那什么是限流呢？用我没读过太多书的话来讲，限流就是限制流量。我们都知道服务器的处理能力是有上限的，如果超过了上限继续放任请求进来的话，可能会发生不可控的后果。而通过限流，在请求数量超出阈值的时候就排队等待甚至拒绝服务，就可以使系统在扛不住过高并发的情况下做到有损服务而不是不服务。

举个例子，如各地都出现口罩紧缺的情况，广州政府为了缓解市民买不到口罩的状况，上线了预约服务，只有预约到的市民才能到指定的药店购买少量口罩。这就是生活中限流的情况，说这个也是希望大家这段时间保护好自己，注意防护 ：）

接下来就跟大家分享下接口限流的常见玩法吧，部分算法用python + redis粗略实现了一下，关键是图解啊！你品，你细品~

固定窗口法
固定窗口法是限流算法里面最简单的，比如我想限制1分钟以内请求为100个，从现在算起的一分钟内，请求就最多就是100个，这分钟过完的那一刻把计数器归零，重新计算，周而复始。



伪代码实现

复制代码
def can_pass_fixed_window(user, action, time_zone=60, times=30):
    """
    :param user: 用户唯一标识
    :param action: 用户访问的接口标识(即用户在客户端进行的动作)
    :param time_zone: 接口限制的时间段
    :param time_zone: 限制的时间段内允许多少请求通过
    """
    key = '{}:{}'.format(user, action)
    # redis_conn 表示redis连接对象
    count = redis_conn.get(key)
    if not count:
        count = 1
        redis_conn.setex(key, time_zone, count)
    if count < times:
        redis_conn.incr(key)
        return True

    return False
 

这个方法虽然简单，但有个大问题是无法应对两个时间边界内的突发流量。如上图所示，如果在计数器清零的前1秒以及清零的后1秒都进来了100个请求，那么在短时间内服务器就接收到了两倍的(200个)请求，这样就有可能压垮系统。会导致上面的问题是因为我们的统计精度还不够，为了将临界问题的影响降低，我们可以使用滑动窗口法。

滑动窗口法
滑动窗口法，简单来说就是随着时间的推移，时间窗口也会持续移动，有一个计数器不断维护着窗口内的请求数量，这样就可以保证任意时间段内，都不会超过最大允许的请求数。例如当前时间窗口是0s~60s，请求数是40，10s后时间窗口就变成了10s~70s，请求数是60。

时间窗口的滑动和计数器可以使用redis的有序集合(sorted set)来实现。score的值用毫秒时间戳来表示，可以利用 当前时间戳 - 时间窗口的大小 来计算出窗口的边界，然后根据score的值做一个范围筛选就可以圈出一个窗口；value的值仅作为用户行为的唯一标识，也用毫秒时间戳就好。最后统计一下窗口内的请求数再做判断即可。



伪代码实现

复制代码
def can_pass_slide_window(user, action, time_zone=60, times=30):
    """
    :param user: 用户唯一标识
    :param action: 用户访问的接口标识(即用户在客户端进行的动作)
    :param time_zone: 接口限制的时间段
    :param time_zone: 限制的时间段内允许多少请求通过
    """
    key = '{}:{}'.format(user, action)
    now_ts = time.time() * 1000
    # value是什么在这里并不重要，只要保证value的唯一性即可，这里使用毫秒时间戳作为唯一值
    value = now_ts 
    # 时间窗口左边界
    old_ts = now_ts - (time_zone * 1000)
    # 记录行为
    redis_conn.zadd(key, value, now_ts)
    # 删除时间窗口之前的数据
    redis_conn.zremrangebyscore(key, 0, old_ts)
    # 获取窗口内的行为数量
    count = redis_conn.zcard(key)
    # 设置一个过期时间免得占空间
    redis_conn.expire(key, time_zone + 1)
    if not count or count < times:
        return True
    return False
复制代码
 

虽然滑动窗口法避免了时间界限的问题，但是依然无法很好解决细时间粒度上面请求过于集中的问题，就例如限制了1分钟请求不能超过60次，请求都集中在59s时发送过来，这样滑动窗口的效果就大打折扣。 为了使流量更加平滑，我们可以使用更加高级的令牌桶算法和漏桶算法。

令牌桶法
令牌桶算法的思路不复杂，它先以固定的速率生成令牌，把令牌放到固定容量的桶里，超过桶容量的令牌则丢弃，每来一个请求则获取一次令牌，规定只有获得令牌的请求才能放行，没有获得令牌的请求则丢弃。



伪代码实现

# 令牌桶法，具体步骤：
# 请求来了就计算生成的令牌数，生成的速率有限制
# 如果生成的令牌太多，则丢弃令牌
# 有令牌的请求才能通过，否则拒绝
复制代码
def can_pass_token_bucket(user, action, time_zone=60, times=30):
    """
    :param user: 用户唯一标识
    :param action: 用户访问的接口标识(即用户在客户端进行的动作)
    :param time_zone: 接口限制的时间段
    :param time_zone: 限制的时间段内允许多少请求通过
    """
    # 请求来了就倒水，倒水速率有限制
    key = '{}:{}'.format(user, action)
    rate = times / time_zone # 令牌生成速度
    capacity = times # 桶容量
    tokens = redis_conn.hget(key, 'tokens') # 看桶中有多少令牌
    last_time = redis_conn.hget(key, 'last_time') # 上次令牌生成时间
    now = time.time()
    tokens = int(tokens) if tokens else capacity
    last_time = int(last_time) if last_time else now
    delta_tokens = (now - last_time) * rate # 经过一段时间后生成的令牌
    if delta_tokens > 1:
        tokens = tokens + tokens # 增加令牌
        if tokens > tokens:
            tokens = capacity
        last_time = time.time() # 记录令牌生成时间
        redis_conn.hset(key, 'last_time', last_time)

    if tokens >= 1:
        tokens -= 1 # 请求进来了，令牌就减少1
        redis_conn.hset(key, 'tokens', tokens)
        return True
    return False
复制代码
 





令牌桶法限制的是请求的平均流入速率，优点是能应对一定程度上的突发请求，也能在一定程度上保持流量的来源特征，实现难度不高，适用于大多数应用场景。

漏桶算法
漏桶算法的思路与令牌桶算法有点相反。大家可以将请求想象成是水流，水流可以任意速率流入漏桶中，同时漏桶以固定的速率将水流出。如果流入速度太大会导致水满溢出，溢出的请求被丢弃。



通过上图可以看出漏桶法的特点是：不限制请求流入的速率，但是限制了请求流出的速率。这样突发流量可以被整形成一个稳定的流量，不会发生超频。

关于漏桶算法的实现方式有一点值得注意，我在浏览相关内容时发现网上大多数对于漏桶算法的伪代码实现，都只是实现了

根据维基百科，漏桶算法的实现理论有两种，分别是基于 meter 的和 基于 queue 的，他们实现的具体思路不同，我大概介绍一下。

基于meter的漏桶
基于 meter 的实现相对来说比较简单，其实它就有一个计数器，然后有消息要发送的时候，就看计数器够不够，如果计数器没有满的话，那么这个消息就可以被处理，如果计数器不足以发送消息的话，那么这个消息将会被丢弃。

那么这个计数器是怎么来的呢，基于 meter 的形式的计数器就是发送的频率，例如你设置得频率是不超过 5条/s ，那么计数器就是 5，在一秒内你每发送一条消息就减少一个，当你发第 6 条的时候计时器就不够了，那么这条消息就被丢弃了。

这种实现有点类似最开始介绍的固定窗口法，只不过时间粒度再小一些，伪代码就不上了。

基于queue的漏桶
基于 queue 的实现起来比较复杂，但是原理却比较简单，它也存在一个计数器，这个计数器却不表示速率限制，而是表示 queue 的大小，这里就是当有消息要发送的时候看 queue 中是否还有位置，如果有，那么就将消息放进 queue 中，这个 queue 以 FIFO 的形式提供服务；如果 queue 没有位置了，消息将被抛弃。

在消息被放进 queue 之后，还需要维护一个定时器，这个定时器的周期就是我们设置的频率周期，例如我们设置得频率是 5条/s，那么定时器的周期就是 200ms，定时器每 200ms 去 queue 里获取一次消息，如果有消息，那么就发送出去，如果没有就轮空。

 

注意，网上很多关于漏桶法的伪代码实现只实现了水流入桶的部分，没有实现关键的水从桶中漏出的部分。如果只实现了前半部分，其实跟令牌桶没有大的区别噢😯
如果觉得上面的都太难，不好实现，那么我墙裂建议你尝试一下redis-cell这个模块！

redis-cell
Redis 4.0 提供了一个限流 Redis 模块，它叫 redis-cell。该模块也使用了漏斗算法，并提供了原子的限流指令。有了这个模块，限流问题就非常简单了。 这个模块需要单独安装，安装教程网上很多，它只有一个指令：CL.THROTTLE
```
CL.THROTTLE user123 15 30 60 1
                ▲    ▲  ▲  ▲ ▲
                |    |  |  | └───── apply 1 operation (default if omitted) 每次请求消耗的水滴
                |    |  └──┴─────── 30 operations / 60 seconds 漏水的速率
                |    └───────────── 15 max_burst 漏桶的容量
                └─────────────────── key “user123” 用户行为
```

执行以上命令之后，redis会返回如下信息：

> cl.throttle laoqian:reply 15 30 60
1) (integer) 0   # 0 表示允许，1表示拒绝
2) (integer) 16  # 漏桶容量
3) (integer) 15  # 漏桶剩余空间left_quota
4) (integer) -1  # 如果拒绝了，需要多长时间后再试(漏桶有空间了，单位秒)
5) (integer) 2   # 多长时间后，漏桶完全空出来(单位秒)
有了上面的redis模块，就可以轻松对付大多数的限流场景了。


https://www.cnblogs.com/xiaozengzeng/p/12642394.html

