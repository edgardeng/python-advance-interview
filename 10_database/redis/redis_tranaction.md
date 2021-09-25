# Redis 事务

Redis 事务可以一次执行多个命令， 并且带有以下三个重要的保证：

* 批量操作在发送 EXEC 命令前被放入队列缓存。
* 收到 EXEC 命令后进入事务执行，事务中任意命令执行失败，其余的命令依然被执行。
* 在事务执行过程，其他客户端提交的命令请求不会插入到事务执行命令序列中。

一个事务从开始到执行会经历以下三个阶段：
 1. 开始事务。
 2. 命令入队。
 3. 执行事务

## 事务命令
* `DISCARD`     取消事务，放弃执行事务块内的所有命令。
* `EXEC`        执行所有事务块内的命令。
* `MULTI`       标记一个事务块的开始。
* `UNWATCH`     取消 WATCH 命令对所有 key 的监视。
* `WATCH key [key ...]` 监视一个(或多个) key ，如果在事务执行之前这个(或这些) key 被其他命令所改动，那么事务将被打断。

## 案例

以 MULTI 开始一个事务， 然后将多个命令入队到事务中， 最后由 EXEC 命令触发事务， 一并执行事务中的所有命令：

```shell script
 MULTI
 SET book-name "Mastering C++ in 21 days" # QUEUED
 GET book-name # QUEUED
 SADD tag "C++" "Programming" "Mastering Series" # QUEUED
 SMEMBERS tag # QUEUED
 EXEC
```

单个 Redis 命令的执行是原子性的

但 Redis 没有在事务上增加任何维持原子性的机制，所以 Redis 事务的执行并不是原子性的
