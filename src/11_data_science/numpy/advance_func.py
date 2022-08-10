import numpy as np


def main():
    x = np.arange(0, 20, 2)
    print(x)
    # y = np.where(x < 5)  # 元组
    # y = np.where(x > 5, x, 5)  # 元组
    # y = np.where(x > 5, x, x*10)
    # print(type(y), y)

    x = np.array([[1, 2], [4, 5], [7, 8]])
    print(x)
    # 若不设置axis，则会自动将数组拉成一条直线，然后进行累加或累乘
    y = np.cumsum(x)
    print(y)
    y = np.cumprod(x)
    print(y)

    y = np.cumsum(x, 0)
    print(y)
    y = np.cumprod(x, 0)
    print(y)

    print('-' * 30)
    y = np.argmin(x)
    print(y)
    y = np.argmax(x)
    print(y)
    print('-' * 30)
    x = np.array([8, 1, 5, 2, 7, 3, 6, 4, 4, 8])
    y = [1, 5, 8, 10]
    print('unique', np.unique(x))
    print('intersect1d', np.intersect1d(x, y))
    print('union1d', np.union1d(x, y))
    print('in1d', np.in1d(x, y))
    print('setdiff1d', np.setdiff1d(x, y))
    print('setxor1d', np.setxor1d(x, y))


if __name__ == '__main__':
    main()
