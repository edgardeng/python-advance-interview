# Redis锁机制

## Redis锁机制的
1 悲观锁

执行操作前假设当前的操作肯定（或有很大几率）会被打断（悲观）。基于这个假设，我们在做操作前就会把相关资源锁定，不允许自己执行期间有其他操作干扰。

Redis不支持悲观锁。Redis作为缓存服务器使用时，以读操作为主，很少写操作，相应的操作被打断的几率较少。不采用悲观锁是为了防止降低性能。

2 乐观锁

执行操作前假设当前操作不会被打断（乐观）。基于这个假设，我们在做操作前不会锁定资源，万一发生了其他操作的干扰，那么本次操作将被放弃。

3. Redis中的锁策略

Redis采用了乐观锁策略（通过watch操作）。乐观锁支持读操作，适用于多读少写的情况！
在事务中，可以通过watch命令来加锁；使用 UNWATCH可以取消加锁；
如果在事务之前，执行了WATCH（加锁），那么执行EXEC 命令或 DISCARD 命令后，锁对自动释放，即不需要再执行 UNWATCH 了

例子

redis锁工具类

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
package com.fly.lock;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;
public class RedisLock {
  //初始化redis池
  private static JedisPoolConfig config;
  private static JedisPool pool;
  static {
    config = new JedisPoolConfig();
    config.setMaxTotal(30);
    config.setMaxIdle(10);
    pool = new JedisPool(config, "192.168.233.200", 6379);
  }
  /**
   * 给target上锁
   * @param target
   **/
  public static void lock(Object target) {
    //获取jedis
    Jedis jedis = pool.getResource();
    //result接收setnx的返回值，初始值为0
    Long result= 0L;
    while (result < 1) {
      //如果target在redis中已经存在，则返回0；否则，在redis中设置target键值对，并返回1
      result = jedis.setnx(target.getClass().getName() + target.hashCode(), Thread.currentThread().getName());
    }
    jedis.close();
  }
  /**
   * 给target解锁
   * @param target
   **/
  public static void unLock(Object target) {
    Jedis jedis = pool.getResource();
    //删除redis中target对象的键值对
    Long del = jedis.del(target.getClass().getName() + target.hashCode());
    jedis.close();
  }
  /**
   * 尝试给target上锁，如果锁成功返回true，如果锁失败返回false
   * @param target
   * @return
   **/
  public static boolean tryLock(Object target) {
    Jedis jedis = pool.getResource();
    Long row = jedis.setnx(target.getClass().getName() + target.hashCode(), "true");
    jedis.close();
    if (row > 0) {
      return true;
    }
    return false;
  }
}
测试类

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
package com.fly.test;
import com.fly.lock.RedisLock;
class Task {
  public void doTask() {
    //上锁
    RedisLock.lock(this);
    System.out.println("当前线程: " + Thread.currentThread().getName());
    System.out.println("开始执行: " + this.hashCode());
    try {
      System.out.println("doing...");
      Thread.sleep(2000);
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
    System.out.println("完成: " + this.hashCode());
    //解锁
    RedisLock.unLock(this);
  }
}
public class Demo {
  public static void main(String[] args) {
    Task task = new Task();
    Thread[] threads = new Thread[5];
    for (Thread thread : threads) {
      thread = new Thread(()->{
        task.doTask();
      });
      thread.start();
    }
  }
}


**Redis锁机制的几种实现方式**

## Redis锁机制的几种实现方式

redis能用的的加锁命令分表是
 *  INCR
 *  SETNX
 *  SET
### 第一种锁命令 INCR
这种加锁的思路是， key 不存在，那么 key 的值会先被初始化为 0 ，然后再执行 INCR 操作进行加一。
然后其它用户在执行 INCR 操作进行加一时，如果返回的数大于 1 ，说明这个锁正在被使用当中。

    1、 客户端A请求服务器获取key的值为1表示获取了锁
    2、 客户端B也去请求服务器获取key的值为2表示获取锁失败
    3、 客户端A执行代码完成，删除锁
    4、 客户端B在等待一段时间后在去请求的时候获取key的值为1表示获取锁成功
    5、 客户端B执行代码完成，删除锁

    $redis->incr($key);
    $redis->expire($key, $ttl); //设置生成时间为1秒

3. 第二种锁SETNX
这种加锁的思路是，如果 key 不存在，将 key 设置为 value
如果 key 已存在，则 SETNX 不做任何动作

    1、 客户端A请求服务器设置key的值，如果设置成功就表示加锁成功
    2、 客户端B也去请求服务器设置key的值，如果返回失败，那么就代表加锁失败
    3、 客户端A执行代码完成，删除锁
    4、 客户端B在等待一段时间后在去请求设置key的值，设置成功
    5、 客户端B执行代码完成，删除锁

    $redis->setNX($key, $value);
    $redis->expire($key, $ttl);

4. 第三种锁SET
上面两种方法都有一个问题，会发现，都需要设置 key 过期。那么为什么要设置key过期呢？如果请求执行因为某些原因意外退出了，导致创建了锁但是没有删除锁，那么这个锁将一直存在，以至于以后缓存再也得不到更新。于是乎我们需要给锁加一个过期时间以防不测。
但是借助 Expire 来设置就不是原子性操作了。所以还可以通过事务来确保原子性，但是还是有些问题，所以官方就引用了另外一个，使用 SET 命令本身已经从版本 2.6.12 开始包含了设置过期时间的功能。

    1、 客户端A请求服务器设置key的值，如果设置成功就表示加锁成功
    2、 客户端B也去请求服务器设置key的值，如果返回失败，那么就代表加锁失败
    3、 客户端A执行代码完成，删除锁
    4、 客户端B在等待一段时间后在去请求设置key的值，设置成功
    5、 客户端B执行代码完成，删除锁

    $redis->set($key, $value, array('nx', 'ex' => $ttl));  //ex表示秒

5. 其它问题
虽然上面一步已经满足了我们的需求，但是还是要考虑其它问题？
1、 redis发现锁失败了要怎么办？中断请求还是循环请求？
2、 循环请求的话，如果有一个获取了锁，其它的在去获取锁的时候，是不是容易发生抢锁的可能？
3、 锁提前过期后，客户端A还没执行完，然后客户端B获取到了锁，这时候客户端A执行完了，会不会在删锁的时候把B的锁给删掉？

6. 解决办法
针对问题1：使用循环请求，循环请求去获取锁
针对问题2：针对第二个问题，在循环请求获取锁的时候，加入睡眠功能，等待几毫秒在执行循环
针对问题3：在加锁的时候存入的key是随机的。这样的话，每次在删除key的时候判断下存入的key里的value和自己存的是否一样

        do {  //针对问题1，使用循环
            $timeout = 10;
            $roomid = 10001;
            $key = 'room_lock';
            $value = 'room_'.$roomid;  //分配一个随机的值针对问题3
            $isLock = Redis::set($key, $value, 'ex', $timeout, 'nx');//ex 秒
            if ($isLock) {
                if (Redis::get($key) == $value) {  //防止提前过期，误删其它请求创建的锁
                    //执行内部代码
                    Redis::del($key);
                    continue;//执行成功删除key并跳出循环
                }
            } else {
                usleep(5000); //睡眠，降低抢锁频率，缓解redis压力，针对问题2
            }
        } while(!$isLock);

7. 另外一个锁
以上的锁完全满足了需求，但是官方另外还提供了一套加锁的算法，这里以PHP为例


    $servers = [
        ['127.0.0.1', 6379, 0.01],
        ['127.0.0.1', 6389, 0.01],
        ['127.0.0.1', 6399, 0.01],
    ];

    $redLock = new RedLock($servers);

    //加锁
    $lock = $redLock->lock('my_resource_name', 1000);

    //删除锁
    $redLock->unlock($lock)

上面是官方提供的一个加锁方法，就是和第6的大体方法一样，只不过官方写的更健壮。所以可以直接使用官方提供写好的类方法进行调用。官方提供了各种语言如何实现锁。

## 参考
* [Redis锁机制的几种实现方式](https://www.cnblogs.com/fengff/p/10913492.html)
* [Distributed locks with Redis](https://redis.io/topics/distlock)
* [](https://mp.weixin.qq.com/s?__biz=MzU0OTk3ODQ3Ng==&mid=2247483893&idx=1&sn=32e7051116ab60e41f72e6c6e29876d9&chksm=fba6e9f6ccd160e0c9fa2ce4ea1051891482a95b1483a63d89d71b15b33afcdc1f2bec17c03c&mpshare=1&scene=1&srcid=0416Kx8ryElbpy4xfrPkSSdB&key=1eff032c36dd9b3716bab5844171cca99a4ea696da85eed0e4b2b7ea5c39a665110b82b4c975d2fd65c396e91f4c7b3e8590c2573c6b8925de0df7daa886be53d793e7f06b2c146270f7c0a5963dd26a&ascene=1&uin=MTg2ODMyMTYxNQ%3D%3D&devicetype=Windows+10&version=62060739&lang=zh_CN&pass_ticket=y1D2AijXbuJ8HCPhyIi0qPdkT0TXqKFYo%2FmW07fgvW%2FXxWFJiJjhjTsnInShv0ap)

https://zhuanlan.zhihu.com/p/112016634

https://blog.csdn.net/t8116189520/article/details/91383256

