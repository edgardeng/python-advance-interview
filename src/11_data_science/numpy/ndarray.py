# -*- coding: utf-8 -*-
# @author: dengxixi
# @date:   2021-09-25
# @file:   11_data_science.numpy
import numpy as np

np.random.seed(0)  # seed for reproducibility


def demo_property():
    print('*' * 30, 'demo_ndarray_property')
    x1 = np.random.randint(10, size=6)  # One-dimensional array
    x2 = np.random.randint(10, size=(3, 4))  # Two-dimensional array
    x3 = np.random.randint(10, size=(3, 4, 5))  # Three-dimensional array

    print("x3 ndim: ", x3.ndim)
    print("x3 shape:", x3.shape)
    print("x3 size: ", x3.size)
    print("dtype:", x3.dtype)
    print("itemsize:", x3.itemsize, "bytes")
    print("nbytes:", x3.nbytes, "bytes")


def demo_index_splice():
    """索引与切片"""
    x1 = np.random.randint(10, size=6)
    print('data:', x1)
    print('索引查询', x1[0], x1[4])
    print('索引查询（负数）', x1[-1], x1[-2])
    x1[0] = 0
    print('赋值后', x1)
    x1[1] = 0.01
    print('赋值后', x1)  # 通过索引可直接赋值，但必须是同一个数据类型的。否则被忽略

    print('切片 x[:5]', x1[:5])
    print('切片 x[5:]', x1[5:])
    print('切片 x[3:5]', x1[3:5])
    print('切片 x[::2]', x1[::2])
    x2 = np.random.randint(10, size=(3, 4))
    print('-' * 20 + 'x2\n', x2)

    print('-' * 20 + 'x2[:3, ::2]\n', x2[:3, ::2])
    print('-' * 20 + 'x2[::-1, ::-1]\n', x2[::-1, ::-1])
    print('-' * 20 + 'x2[:, 0]\n', x2[:, 0])  # first column of x2
    x3 = x2[:2, :2]
    print('-' * 20 + 'x3 = x2[:2, :2]\n', x3)  # 2x2
    x3[1] = 0
    print('-' * 20 + 'x3被修改后的x3\n', x3)
    print('-' * 20 + 'x3被修改后的x2\n', x2)  # ndarray的切片是 赋值引用
    x2_sub_copy = x2[:2, :2].copy()  # 通过copy函数进行 直接赋值
    x2_sub_copy[1] = 100
    print('-' * 20 + '拷贝并被修改后的x2_sub\n', x2_sub_copy)
    print('-' * 20 + '拷贝并被修改后的x2\n', x2)
    print('-' * 20 + 'python中list切片是浅拷贝\n')
    arr = list(range(10))
    arr2 = arr[:3]
    print(arr, arr2)
    arr2[1] = 0
    print(arr, arr2)  # python种的list是


def demo_reshape():
    x = np.arange(1, 2 * 3 * 5 + 1)
    x2 = x.reshape((6, 5))  # reshape的结果是引用赋值。，no-copy view of the initial array
    x2[1] = -1
    print('-' * 20 + 'x\n', x)
    print('-' * 20 + 'x reshape > (15,4)\n', x2)
    print('-' * 20 + 'x reshape > (5,3,2)\n', x.reshape((5, 3, 2)))

    x = np.array([1, 2, 3])
    # x.reshape((1, 3))  # array([[1, 2, 3]])
    print(x[np.newaxis, :])  # row vector via newaxis # array([[1, 2, 3]])
    # x.reshape((3, 1))  # array([[1],[2],[3]])
    # column vector via newaxis
    print(x[:, np.newaxis])  # array([[1],[2],[3]])

    b = np.expand_dims(x, axis=1)  # 引用赋值
    print('-' * 20 + 'expand_dims 升维 b\n', b)
    print('-' * 20 + 'expand_dims 升维 x\n', x)
    c = np.squeeze(b)
    print('-' * 20 + 'squeeze 降维\n', c)  # 数据引用赋值

    x = np.arange(1, 7).reshape((1, 2, 3))
    print('-' * 20 + ' 降维前 x\n', x)
    y = np.ravel(x)  # 将多维数组拉平（一维） 数据引用赋值
    # print(x.reshape(-1)) # 和ravel效果一样
    # squeeze # 除去多维数组中，维数为1的维度，如315降维后3*5
    print(x.reshape(-1, 3))  # 变形为 ？*3维
    print(x.reshape(2, -1))  # 变形为 2*？维
    print('-' * 20 + '拉平并复制数据 x\n', x.flatten())


def demo_concat():
    x = np.array([1, 2, 3])
    y = np.array([3, 2, 1])
    con1 = np.concatenate([x, y])  # [1 2 3 3 2 1]
    print('-' * 20 + 'concatenate([x,y])\n', con1)
    z = np.array([99, 99, 99])
    con2 = np.concatenate([x, y, z])  # [ 1  2  3  3  2  1 99 99 99]
    print('-' * 20 + 'concatenate([x, y, z])', con2)

    grid = np.array([[1, 2, 3],
                     [4, 5, 6]])
    con3 = np.concatenate([grid, grid])
    print('-' * 20 + '2 dims concatenate([x, y])', con3)
    con4 = np.concatenate([grid, grid], axis=1)
    print('-' * 20 + '2 dims concatenate([x, y,axis=1])', con4)

    x = np.array([9, 9, 9])
    grid = np.array([[1, 1, 1],
                     [1, 1, 1]])
    con5 = np.vstack([x, grid])  # [[9 9 9] [1 1 1] [1 1 1]]
    print('-' * 20 + 'mix dims vstack([x, y]) \n', con5)
    y = np.array([[99],
                  [99]])
    con6 = np.hstack([grid, y])  # [[ 1  1  1 99] [ 1  1  1 99]]
    con6[0] = -1
    print('-' * 20 + 'mix dims hstack([x, y]) \n', con6)

    a = np.array([[1, 1], [2, 2], [3, 3]])
    b = np.insert(a, 1, 5)  # [1 5 1 2 2 3 3]
    c = np.insert(a, 1, [-1, -1])  # [ 1 -1 -1  1  2  2  3  3]
    d = np.insert(a, 1, [-1, -1], axis=0)  # [[ 1  1][-1 -1][ 2  2][ 3  3]]
    e = np.insert(a, 1, [0], axis=1)  # [[1 0 1][2 0 2][3 0 3]]
    f = np.insert(a, 1, [-1, -2, -3], axis=1)  # [[ 1 -1  1][ 2 -2  2][ 3 -3  3]]
    g = np.insert(a, 1, [[-1], [-2], [-3]], axis=1)
    # [[ 1 -1 -2 -3  1] [ 2 -1 -2 -3  2] [ 3 -1 -2 -3  3]]
    h = np.insert(a, [1], [[-1], [-2], [-3]], axis=1)
    # [[ 1 -1  1]
    #  [ 2 -2  2]
    a = np.array([1, 1, 2, 2, 3, 3])
    np.insert(a, [2, 2], [5, 6])
    # array([1, 1, 5, 6, 2, 2, 3, 3])
    np.insert(a, [2, 3], [5, 6])
    # array([1, 1, 5, 2, 6, 2, 3, 3])
    np.insert(a, (2, 4), [5, 6])
    # array([1, 1, 5, 2, 2, 6, 3, 3])
    np.insert(a, [2, 2], [7.13, False])  # type cast
    # array([1, 1, 7, 0, 2, 2, 3, 3])


def demo_split():
    """split and delete """
    a = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    x1, x2, x3 = np.split(a, [1, 2])
    # array([0]),,array([1]),array([2, 3, 4, 5, 6, 7, 8, 9])
    x = np.split(a, 2)
    # [array([0, 1, 2, 3, 4]), array([5, 6, 7, 8, 9])]
    np.split(a, (4,))
    # [array([0, 1, 2, 3]), array([4, 5, 6, 7, 8, 9])]
    np.split(a, (0, 3, 5))
    # [array([], dtype=int32), array([0, 1, 2]), array([3, 4]), array([5, 6, 7, 8, 9])]
    a = np.arange(16).reshape((4, 4))
    up_down = np.vsplit(a, [2])
    # [array([[0, 1, 2, 3], [4, 5, 6, 7]]), array([[ 8,  9, 10, 11], [12, 13, 14, 15]])]
    left_right = np.hsplit(a, [2])
    # [array([[ 0,  1],[ 4,  5],[ 8,  9],[12, 13]]), array([[ 2,  3],[ 6,  7],[10, 11],[14, 15]])]
    np.delete(a, 1)
    # array([ 0,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15])
    np.delete(a, 1, axis=0)
    # array([[ 0,  1,  2,  3],[ 8,  9, 10, 11],[12, 13, 14, 15]])
    np.delete(a, 1, axis=1)
    np.delete(a, (0, 2), axis=1)
    np.delete(a, slice(0, 2), axis=1)  # 删除连续的项
    np.delete(a, slice(0, 4, 2), axis=1)  # 删除偶数项


if __name__ == '__main__':
    # demo_index_splice()
    # demo_reshape()
    # demo_concat()
    demo_split()
    pass

