# 使用Python操作Redis

## 安装依赖

使用pip进行安装：` pip install redis `

## Redis的基本操作

导入依赖， 创建链接

```python
from redis import Redis
redis = Redis(host='localhost', port=6379, db=0)
```

一、字符串类型string
我们先通过例子看一下如何使用string类型数据

复制代码


##### 单个string
result = client.set('Mark', 100)
print(result)    # 输出：True
age = client.get('Mark')
print(age.decode())   # 输出：100

##### 多个string
student = {
    'name': 'zeng',
    'age': '22'
}
result1 = client.mset(student)
print(result1)   # True
stu = client.mget(['name', 'age'])
print(stu)   # 输出：[b'zeng', b'22']

##### 删除操作
d = client.delete('name', 'age')
print(d)  # 2
result = client.get('name')
print(result)  # None
复制代码
上面的例子中分别对单个string、多个string进行了举例，其中涉及到赋值和取值的方法，我们来看一下具体的介绍：

set()方法：单个string操作方法，用于设置给定 key 的值。如果 key 已经存储其他值， SET 就覆写旧值，且无视类型；
get()方法：单个string操作，用于获取指定 key 的值，如果key不存在，返回nil，如果key储存的值不是字符串类型，返回一个错误；
decode()方法：这个大家应该都知道，用于解码；
mset()：多个string操作，用于同时设置一个或多个key-value对；
mget()：多个string操作，返回所有给定key的值；
delete()：删除数据，可以根据key来指定删除数据；
二、列表类型list
import redis
client = redis.StrictRedis(host='localhost', port=6379, db=0)
lpush()方法：令将一个或多个值插入到列表头部，如果 key 不存在，一个空列表会被创建并执行 LPUSH 操作，当 key存在但不是列表类型时，返回一个错误；
注意：在Redis 2.4版本以前的 LPUSH 命令，都只接受单个 value 值；

复制代码
# 插入一个元素
result = client.lpush('lsts', 'name')
print(result)

# 创建列表
lsts = ('name', 'age', 'class', 'score')

# 插入多个元素
result = client.lpush('lsts', *lsts)
print(result)    # 4
复制代码
lrange()方法：返回列表中指定区间内的元素，区间以偏移量START和END指定，其中0表示列表的第一个元素，1表示列表的第二个元素，以此类推，以-1表示列表的最后一个元素， -2表示列表的倒数第二个元素，以此类推；

# 先加入进入的元素在后面，后加入的元素在前面
result = client.lrange('lsts', 0, -1)
print(result)   # [b'score', b'class', b'age', b'name']
lpop()方法：用于移除并返回列表的第一个元素；

# 从左边删除一个元素
result = client.lpop('lsts')
print(result)    # b'score'
三、集合类型set
import redis
client = redis.StrictRedis(host='localhost', port=6379, db=0)
sadd()：将一个或多个成员元素加入到集合中，已经存在于集合的成员元素将被忽略；

sets = ('name', 'age', 'class', 'score')
result = client.sadd('new_sets', *sets)
print(result)  # 4
smembers()：判断成员元素是否是集合的成员；

result = client.smembers('new_sets')
print(result)
srem()：用于移除集合中的一个或多个成员元素，不存在的成员元素会被忽略；

result = client.srem('new_sets', 'address')
print(result)   # 1
四、哈希类型hash
import redis
client = redis.StrictRedis(host='localhost', port=6379, db=0)
hset()：用于为哈希表中的字段赋值 ，如果哈希表不存在，一个新的哈希表被创建并进行HSET操作；

client.hset("hash1", "k1", "v1")
client.hset("hash1", "k2", "v2")
hkeys()：用于获取哈希表中的所有域（field）；

print(client.hkeys("hash1")) # [b'k1', b'k2']
hget()：用于返回哈希表中指定字段的值；

print(client.hget("hash1", "k1")) # b'v1'
hmget()：用于返回哈希表中，一个或多个给定字段的值；

print(client.hmget("hash1", "k1", "k2")) # [b'v1', b'v2']
五、有序集合类型 sorted set
import redis
client = redis.StrictRedis(host='localhost', port=6379, db=0)
zadd(name, *args, **kwargs) ：在name对应的有序集合中添加元素；

d = {'Join': '20'}
result = client.zadd("zset1", d)
print(result)  # 1
zcard(name)：获取name对应的有序集合元素的数量；

result = client.zcard("zset1")
print(result) 
zcount(name, min, max)：获取name对应的有序集合中分数 在 [min,max] 之间的个数；

client.zcount("zset1", 0, 1)
zincrby(name, value, amount) ：自增name对应的有序集合的 name 对应的分数；

print(client.zincrby("zset1", 1, '20'))
 

[官网地址](https://github.com/andymccurdy/redis-py)