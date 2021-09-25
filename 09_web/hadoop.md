#
## HDFS
1. 保存多个副本，且提供容错机制，比如一个副本丢失，可以通过其他副本来恢复，默认存3份
2. 适合大数据的处理。HDFS默认将文件分割成block，每个block：64M
3. 一次写入，多次读取，文件一旦写入不能修改，只能追加
4. 不适合小文件处理

![](https://pic2.zhimg.com/80/v2-12bac7206f243ab217e58a23a555da47_720w.jpg?source=1940ef5c)

* NameNode: Master节点（主节点），可以看作是分布式文件系统中的管理者，主要负责管理文件系统的命名空间、集群配置信息和存储块的复制等。NameNode会将文件系统的Meta-data存储在内存中，这些信息主要包括了文件信息、每一个文件对应的文件块的信息和每一个文件块在DataNode的信息等。

* DataNode: 是Slave节点（从节点），是文件存储的基本单元，它将Block存储在本地文件系统中，保存了Block的Meta-data，同时周期性地将所有存在的Block信息发送给NameNode。

*CLient: 切分文件；访问HDFS；与NameNode交互，获得文件位置信息；与DataNode交互，读取和写入数据。 

* Block是HDFS中的基本读写单元；HDFS中的文件都是被切割为block（块）进行存储的；这些块被复制到多个DataNode中；块的大小（通常为64MB）和复制的块数量在创建文件时由Client决定。
# Hadoop安装

