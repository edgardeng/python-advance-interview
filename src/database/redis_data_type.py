"""
Redis Test Demo 测试案例

redis==3.5.3
Redis客户端 5.0
"""
import json
from redis import Redis
import datetime

redis = Redis(host='localhost', port=6380, db=0)


def string_cache():
    '''
     Redis String 操作
     set(name, value, ex=None, px=None, nx=False, xx=False) 参数：
        ex，过期时间（秒）
        px，过期时间（毫秒）
        nx，如果设置为True，则只有name不存在时，当前set操作才执行,同setnx(name, value)
        xx，如果设置为True，则只有name存在时，当前set操作才执行
     delete(name)     删除某个键
     '''

    data = {'a': 1, 'b': 2}
    redis.set('cache-key', json.dumps(data))
    print(' set cache-key with value:', data)
    result = json.loads(redis.get('cache-key'))
    print(' get cache-key with value:', result)
    # redis.setex('cache-key-x', 'I will disappear after 1s', 1)      # setex(name, value, time) # 设置过期时间（秒）
    # redis.psetex('cache-key-x', 'I will disappear after 1s', 1000)  # psetex(name, time_ms, value) # 设置过期时间（豪秒）
    # 批量设置值
    # redis.mset(name_1='zhangsan', name_2='lisi')
    redis.mset({"name1": 'zhangsan', "name2": 'lisi'})
    # 批量获取
    print(redis.mget("name1", "name2"))
    li = ["name1", "name2"]
    print(redis.mget(li))

    # getset(name, value) 设置新值，打印原值
    print(redis.getset("name1", "wangwu"))  # 输出:zhangsan
    print(redis.get("name1"))  # 输出:wangwu

    # getrange(key, start, end)根据字节获取子序列
    redis.set("name", "zhangsan")
    print(redis.getrange("name", 0, 3))  # 输出:zhan

    # setrange(name, offset, value)  修改字符串内容，从指定字符串索引开始向后替换，如果新值太长时，则向后添加
    redis.set("name", "zhangsan")
    redis.setrange("name", 1, "z")
    print(redis.get("name"))  # 输出:zzangsan
    redis.setrange("name", 6, "zzzzzzz")
    print(redis.get("name"))  # 输出:zzangszzzzzzz

    ''' 
      setbit(name, offset, value) 对二进制表示位进行操作
        name:redis的name
        offset，位的索引（将值对应的ASCII码变换成二进制后再进行索引）
        value，值只能是 1 或 0 '''

    str = "345"
    redis.set("name", str)
    for i in str:
        print(i, ord(i), bin(ord(i)))  # 输出 值、ASCII码中对应的值、对应值转换的二进制
    '''
    输出:
        3 51 0b110011
        4 52 0b110100
        5 53 0b110101
    '''

    redis.setbit("name", 6, 0)  # 把第7位改为0，也就是3对应的变成了0b110001
    print(redis.get("name"))  # 输出：145

    # 获取name对应值的二进制中某位的值(0或1)
    redis.set("name", "3")  # 对应的二进制0b110011
    print(redis.getbit("name", 5))  # 输出:0
    print(redis.getbit("name", 6))  # 输出:1
    # bitcount(key, start=None, end=None)

    # bitcount(key,start, end) 获取对应二进制中1的个数
    redis.set("name", "345")  # 0b110011 0b110100 0b110101
    print(redis.bitcount("name", start=0, end=1))  # 输出:7

    # strlen(name) 返回name对应值的字节长度（一个汉字3个字节）
    redis.set("name", "zhangsan")
    print(redis.strlen("name"))  # 输出:8
    # incr(self, name, amount=1)

    # 自增mount对应的值，当mount不存在时，则创建mount＝amount，否则，则自增,amount为自增数(整数)
    # redis.get("mount")
    print(redis.incr("mount", amount=2))  # 输出:2
    print(redis.incr("mount"))  # 输出:3
    print(redis.incr("mount", amount=3))  # 输出:6
    print(redis.incr("mount", amount=6))  # 输出:12
    print(redis.get("mount"))  # 输出:b'12'
    # incrbyfloat(self, name, amount=1.0) amount为自增数(浮点数)

    # decr(self, name, amount=1) 自减name对应的值,当name不存在时,则创建name＝amount，否则，则自减，amount为自增数(整数)
    print(redis.decr("mount", amount=2))
    redis.delete("mount")

    # append(name, value) 在name对应的值后面追加内容
    redis.set("name", "zhangsan")
    print(redis.get("name"))  # 输出:'zhangsan
    redis.append("name", "lisi")
    print(redis.get("name"))  # 输出:zhangsanlisi


def hash_operate_cache():
    """
    Hash (在内存中类似于一个name对应一个dic来存储) 操作
        hset(name, key, value)   name对应的hash中设置一个键值对（不存在，则创建，否则，修改）
        hget(name,key)           在name对应的hash中根据key获取value
        hgetall(name)
        hmset(name, mapping)    [deprecated] 在name对应的hash中批量设置键值对,mapping:字典
        hmget(name, keys, *args)    在name对应的hash中获取多个key的值
        hlen(name)                  获取hash中键值对的个数
        hkeys(name)                 获取hash中所有的key的值
        hvals(name)                 获取hash中所有的value的值
        hexists(name, key)          是否存在当前传入的key
        hdel(name,*keys)            删除指定name对应的key所在的键值对
        hincrby(name, key, amount=1)            自增hash中key对应的值，不存在则创建key=amount(amount为整数)
        hincrbyfloat(name, key, amount=1.0)     自增hash中key对应的值，不存在则创建key=amount(amount为浮点数)
        hscan(name, cursor=0, match=None, count=None)
        hscan_iter(name, match=None, count=None)
    :return:
    """

    redis.hset("dic_name", "a1", "aa")
    redis.hset("dic_name", "a1", "aa")
    print(redis.hget("dic_name", "a1"))  # 输出:aa
    print('获取name对应hash的所有键值: ', redis.hgetall("dic_name"))

    dic = {"a1": "aa", "b1": "bb"}
    redis.hset("dic_name", mapping=dic)
    print(redis.hget("dic_name", "b1"))  # 输出:bb

    # 在name对应的hash中获取多个key的值
    li = ["a1", "b1"]
    print(redis.hmget("dic_name", li))
    print(redis.hmget("dic_name", "a1", "b1"))

    dic = {"a1": "aa", "b1": "bb"}
    redis.hmset("dic_name", dic)

    # hlen(name) 获取hash中键值对的个数
    print(redis.hlen("dic_name"))

    # hkeys(name) 获取hash中所有的key的值
    print(redis.hkeys("dic_name"))

    # hvals(name) 获取hash中所有的value的值
    print(redis.hvals("dic_name"))

    # 检查name对应的hash是否存在当前传入的key
    print(redis.hexists("dic_name", "a1"))  # 输出:True

    # 删除指定name对应的key所在的键值对
    redis.hdel("dic_name", "a1")

    # 自增hash中key对应的值，不存在则创建key=amount(amount为整数)
    print(redis.hincrby("demo", "a", amount=2))
    print(redis.hincrbyfloat("demo", "a", amount=2.1))


def list_operate_cache():
    """
    List (在内存中按照一个name对应一个List来存储)操作
        lpush(name,values)
        rpush(name,values)      # 同lpush，但每个新的元素都添加到列表的最右边
        lpushx(name,value)      # 在name对应的list中添加元素，只有name已经存在时，值添加到列表的最左边
        rpushx(name,value)      # 在name对应的list中添加元素，只有name已经存在时，值添加到列表的最右边
        llen(name)
        linsert(name, where, refvalue, value))  # 在name对应的列表的某一个值前或后插入一个新值
            name: redis的name
             where: BEFORE（前）或AFTER（后）
             refvalue: 列表内的值
             value: 要插入的数据 
        lset(name, index, value)    # 对list中的某一个索引位置重新赋值
        lrem(name, count, value)   # 删除name对应的list中的指定值value
            count=0 删除列表中所有的指定值；
            count=2 从前到后，删除2个；
            count=-2 从后向前，删除2个'''
        lpop(name)                  # 移除列表的左侧第一个元素，返回值则是第一个元素
        blpop(keys, timeout)
        brpop
        # lindex(name, index) 根据索引获取列表内元素
        # lrange(name, start, end)分片获取元素
        # ltrim(name, start, end) 移除列表内没有在该索引之内的值
        rpoplpush(src, dst)             # 从一个列表src取出最右边的元素，同时将其添加至另一个列表dst的最左边
        brpoplpush(src, dst, timeout=0) # 同上，取数据的列表没元素后的阻塞时间，0为一直阻塞
    :return:
    """
    redis.lpush("list_name", 1)
    redis.lpush("list_name", 2, 3, 4, 5)  # 保存在列表中的顺序为5，4，3，2, 1
    print(redis.llen("list_name"))  # 输出：5
    redis.linsert("list_name", "BEFORE", "2", "SS")  # 在列表内找到第一个元素2，在它前面插入SS
    redis.lset("list_name", 0, "bbb")  # 重新赋值
    redis.lrem("list_name", 0, "SS")  # 删除所有的SS
    # print(redis.get("list_name"))

    print(redis.lpop("list_name"))  # 移除并返回列表的左侧第一个元素
    redis.blpop("list_name", timeout=1)  # 如果没有，则设置阻塞时间

    print(redis.lindex("list_name", 1))
    print(redis.lrange("list_name", 0, -1))
    redis.ltrim("list_name", 0, 2)
    print(redis.lrange("list_name", 0, -1))

    # redis.rpoplpush("list_name", "list_name1")
    # 同rpoplpush，多了个timeout, timeout：
    redis.brpoplpush("list_name", "list_name1", timeout=0)
    print('*' * 30, 'after brpoplpush')
    print(redis.lrange("list_name", 0, -1))
    print(redis.lrange("list_name1", 0, -1))

    # 将多个列表排列,按照从左到右去移除各个列表内的元素
    redis.lpush("list_name", 3, 4, 5)
    redis.lpush("list_name1", 3, 4, 5)
    print('*' * 30)
    for _ in range(10):
        print(redis.blpop(["list_name", "list_name1"], timeout=2))
        print(redis.lrange("list_name", 0, -1), redis.lrange("list_name1", 0, -1))
        print(datetime.datetime.now())
    redis.delete("list_name")
    redis.delete("list_name1")


def set_operate_cache():
    """
    4、Set 操作

    Set集合就是不允许重复的列表

    sadd(name,values) 给name对应的集合中添加元素
    smembers(name)    获取name对应的集合的所有成员
    scard(name)       获取name对应的集合中的元素个数
    sdiff(keys, *args)                  在第一个name对应的集合中且不在其他name对应的集合的元素集合
    sinterstore(dest, keys, *args)      # 获取多个name对应集合的并集，再讲其加入到dest对应的集合中
    sismember(name, value)              # 检查value是否是name对应的集合内的元素
    smove(src, dst, value)              # 将某个元素从一个集合中移动到另外一个集合
    spop(name)                          # 从集合的右侧移除一个元素，并将其返回
    srandmember(name, numbers)          # 从name对应的集合中随机获取numbers个元素
    srem(name, values)                  # 删除name对应的集合中的某些值
    sunion(keys, *args)                 # 获取多个name对应的集合的并集
    sunionstore(dest, keys, *args)

    """
    #
    redis.sadd("set_name", "aa")
    redis.sadd("set_name", "aa", "bb", 'cc')
    print(redis.smembers("set_name"))

    print(redis.scard("set_name"))

    redis.sadd("set_name", "aa", "bb")
    redis.sadd("set_name1", "bb", "cc")
    redis.sadd("set_name2", "bb", "cc", "dd")

    print(redis.sdiff("set_name", "set_name1", "set_name2"))  # 差集： a-b-c = 输出:｛aa｝
    # sdiffstore(dest, keys, *args)

    # 相当于把sdiff获取的值加入到dest对应的集合中
    # sinter(keys, *args)

    # 获取多个name对应集合的并集
    redis.sadd("set_name", "aa", "bb")
    redis.sadd("set_name1", "bb", "cc")
    redis.sadd("set_name2", "bb", "cc", "dd")

    print(redis.sinter("set_name", "set_name1", "set_name2"))  # 输出:｛bb｝
    print(redis.srandmember("set_name2", 2))
    print(redis.srem("set_name2", "bb", "dd"))
    print(redis.sunion("set_name", "set_name1", "set_name2"))  # 和集


def zset_operate_cache():
    """
    4、ZSet 有序集合 操作
    在集合的基础上，为每元素排序，元素的排序需要根据另外一个值来进行比较，所以，对于有序集合，每一个元素有两个值，即：值和分数，分数专门用来做排序。

        zadd(name, *args, **kwargs)              # 获取多个name对应的集合的并集，并将结果保存到dest对应的集合中
        zunionstore(dest, keys, aggregate=None)
        zcard(name)                             # 获取有序集合内元素的数量
        zcount(name, min, max)                  # 获取有序集合内元素的数量
        zincrby(name, value, amount)            # 自增有序集合内value对应的分数
        zrange( name, start, end, desc=False, withscores=False, score_cast_func=float)  # 按照索引范围获取name对应的有序集合的元素
            参数：
                name    redis的name
                start   有序集合索引起始位置
                end     有序集合索引结束位置
                desc    排序规则，默认按照分数从小到大排序
                withscores  是否获取元素的分数，默认只获取元素的值
                score_cast_func 对分数进行数据转换的函数
        zrevrange(name, start, end, withscores=False, score_cast_func=float)   # 同zrange，集合是从大到小排序的
        zrank(name, value)、zrevrank(name, value)    # 获取value值在name对应的有序集合中的排行位置（从0开始）
        zrevrank                                    # 从大到小排序
        zscore(name, value)                         # 获取name对应有序集合中 value 对应的分数
        zrem(name, values)                          # 删除name对应的有序集合中值是values的成员
        zremrangebyrank(name, min, max) # 根据排行范围删除
        zremrangebyscore(name, min, max) # 根据分数范围删除
        zinterstore(dest, keys, aggregate=None)

    """

    a_set = {"a1": 6, "a2": 2, "a3": 5}
    redis.zadd("zset_name", a_set)  # 在name对应的有序集合中添加元素
    # redis.zadd('zset_name1', b1=10, b2=5)
    print(redis.zcard("zset_name"))  # 返回集合中元素的数量
    print(redis.zscan("zset_name"))

    # 获取有序集合中分数在[min,max]之间的个数
    print('zcount 1-5: ', redis.zcount("zset_name", 1, 5))
    redis.zincrby("zset_name", 2, 'a1')  # 自增zset_name对应的有序集合里a1对应的分数
    print(redis.zscan("zset_name"))
    aa = redis.zrange("zset_name", 0, 1, desc=False, withscores=True, score_cast_func=int)
    print(aa)

    # 获取value值在name对应的有序集合中的排行位置（从0开始）
    print('zrank:', redis.zrank("zset_name", "a2"))
    print('zrevrank:',redis.zrevrank("zset_name", "a2"))  # 从大到小排序

    # 获取name对应有序集合中 value 对应的分数
    print('zscore:', redis.zscore("zset_name", "a1"))

    # 删除name对应的有序集合中值是values的成员
    redis.zrem("zset_name", "a1", "a2")
    print('zset_name:', redis.zscan("zset_name"))
    redis.zadd("zset_name", a_set)
    redis.zadd('zset_name1', {"a1": 7, "b1": 10, "b2": 5})
    print('zset_name:', redis.zscan("zset_name"))
    print('zset_name1:', redis.zscan("zset_name1"))


    # 获取两个有序集合的交集并放入dest集合，如果遇到相同值不同分数，则按照aggregate进行操作
    # aggregate的值为: SUM  MIN  MAX
    redis.zinterstore("zset_name2", ("zset_name1", "zset_name"), aggregate="MAX")
    print(redis.zscan("zset_name2"))
    redis.delete('zset_name', 'zset_name1', 'zset_name2')


def list_queue():
    print(' push data to queue')
    # https://segmentfault.com/a/1190000008404117


def redis_usage():
    """
    redis其他常用操作

        delete(*names) # 根据name删除redis中的任意数据类型
        exists(name) # 检测redis的name是否存在
        keys(pattern='*') # 根据* ？等通配符匹配获取redis的name
        expire(name ,time) # 为某个name设置超时时间
        rename(src, dst) # 重命名
        move(name, db)) # 将redis的某个值移动到指定的db下
        randomkey() # 随机获取一个redis的name（不删除）
        type(name) # 获取name对应值的类型
    """
    redis.set('key_1', 1)
    redis.exists('key_1')
    redis.expire('key_1', 2)
    redis.rename('key_1', 'key_2')
    redis.type('key_2')
    print(redis.get('key_1'))
    redis.delete('key_2')


if __name__ == '__main__':
    redis_usage()
    # string_cache()
    # hash_operate_cache()
    # list_operate_cache()
    # set_operate_cache()
    zset_operate_cache()
