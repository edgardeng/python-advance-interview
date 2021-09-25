# Numpy

## How to build a NDArray
> NDArray 是NumPy最基本的数据结构 


### 使用numpy生成随机数的几种方式

1. np.random.random(10)         生成指定形状0-1的随机数组
2. np.random.rand(a)            生成和?一样形状,0-1的随机数组
3. np.random.randint(1,10,20)   生成指定数值范围内的随机数值
4. np.random.randn(10)          生成服从均值0标准差1的标准正态分布随机数值
5. np.random.normal()           生成指定均值和标准差的正态分布随机数值
6. np.random.uniform()          生成均匀分布随机数组
7. np.random.seed()             随机种子
8. np.random.shuffle()          打乱数组元素顺序
9. np.random.choice()           按照概率从指定数组中，随机抽出某个数组


### 使用numpy生成特殊数组的几种方式

| 特殊矩阵	     | 解释  |
|:----|:----|
|np.asarray(data)	|拷贝data矩阵 |
|np.ones(n)|生成一个长度为n的一维数组，元素都是1|
|np.ones( (M, N) )|生成一个M行N列的二维矩阵，元素都是1|
|np.ones_like( data )|生成一个与矩阵data相同形状的矩阵，元素都是1|
|np.zeros(n)|生成一个长度为n的一维数组，元素都是0|
|np.zeros( (M, N) )|生成一个M行N列的二维矩阵，元素都是0|
|np.zeros_like( data )|生成一个与矩阵data相同形状的矩阵，元素都是0|
|np.empty(n)|生成一个长度为n的未初始化的一维数组|
|np.empty(n,dtype)|生成一个M行N列的未初始化的二维矩阵|
|np.empty(data)|生成一个与矩阵data相同形状的未初始化的矩阵|
|np.eye(n)	|生成一个n*n的单位矩阵（对角线元素为1，其余为0）|
|np.arange(n)|生成从0 到（n-1）的一维数组，步数为1|
|np.arange(begin, end)|生成从 begin 到（end-1）的一维数组，步数为1|
|np.arange(begin, end, step)|生成从 begin 到（end-step）的一维数组，步数为step |

