# Numpy

## NDArray
> NDArray 是NumPy最基本的数据结构 
> 
### NumPy Standard Data Types 标准数据类型

The standard NumPy data types are listed in the following table.


|Data type	|Description|
|:----|:----|
|bool	    |Boolean (True or False) stored as a byte|
|int	    |Default integer type (same as C long; normally either int64 or int32)|
|intc	    |Identical to C int (normally int32 or int64)|
|intp	    |Integer used for indexing (same as C ssize_t; normally either int32 or int64)|
|int8	    |Byte (-128 to 127)|
|int16	    |Integer (-32768 to 32767)|
|int32	    |Integer (-2147483648 to 2147483647)|
|int64	    |Integer (-9223372036854775808 to 9223372036854775807)|
|uint8	    |Unsigned integer (0 to 255)|
|uint16	    |Unsigned integer (0 to 65535)|
|uint32	    |Unsigned integer (0 to 4294967295)|
|uint64	    |Unsigned integer (0 to 18446744073709551615)|
|float_	    |Shorthand for float64.|
|float16	|Half precision float: sign bit, 5 bits exponent, 10 bits mantissa|
|float32	|Single precision float: sign bit, 8 bits exponent, 23 bits mantissa|
|float64	|Double precision float: sign bit, 11 bits exponent, 52 bits mantissa|
|complex_	|Shorthand for complex128.|
|complex64	|Complex number, represented by two 32-bit floats|
|complex128	|Complex number, represented by two 64-bit floats|


### Attributes

Each array has attributes:

* ``ndim`` the number of dimensions
* ``shape`` the size of each dimension
* ``size`` the total size of the array
* ``dtype`` the data type of the array
* ``itemsize``,  lists the size (in bytes) of each array element
* ``nbytes``,  lists the total size (in bytes) of the array

```python

import numpy as np
np.random.seed(0)  # seed for reproducibility
x1 = np.random.randint(10, size=6)  # One-dimensional array
x2 = np.random.randint(10, size=(3, 4))  # Two-dimensional array
x3 = np.random.randint(10, size=(3, 4, 5))  # Three-dimensional array

print("x3 ndim: ", x3.ndim)
print("x3 shape:", x3.shape)
print("x3 size: ", x3.size)

print("dtype:", x3.dtype)
print("itemsize:", x3.itemsize, "bytes")
print("nbytes:", x3.nbytes, "bytes")
```

#### Array Indexing: Accessing Single Elements 索引

In a one-dimensional array, the 𝑖𝑡ℎ value (counting from zero) can be accessed by specifying the desired index in square brackets, just as with Python lists:

To index from the end of the array, you can use negative indices:

```python
x1 = np.random.randint(10, size=6)  
print(x1)
print(x1[0], x1[4])
print(x1[-1], x1[-2])

```

In a multi-dimensional array, items can be accessed using a comma-separated tuple of indices:

```python
x2 = np.random.randint(10, size=(3, 4))
print(x2)
print(x2[0, 0])
print(x2[2, -1])

```

Values can also be modified using any of the above index notation:

```python
x2[0, 0] = 12
print(x2)
```

> Keep in mind that, unlike Python lists, NumPy arrays have a fixed type. 
> If you attempt to insert a floating-point value to an integer array, the value will be silently truncated.
> 通过索引可直接赋值，但必须是同一个数据类型的。

```python
x1[0] = 3.14159 
print(x1)
```

#### Array Slicing: Accessing Subarrays 切片

The NumPy slicing syntax follows that of the standard Python list; to access a slice of an array x, use this:`x[start:stop:step]`

```python
    # One-dimensional subarrays
    x = np.arange(10)
    print('x', x)
    print('x[:5]', x[:5])
    print('x[5:]', x[5:])
    print('x[3:5]', x[3:5])
    print('x[::2]', x[::2])
    print('x[1::2]', x[1::2])
    print('x[::-1]', x[::-1])
    print('x[5::-2]', x[5::-2])
    # Multi-dimensional slices 
    x2 = np.random.randint(10, size=(3, 4))
    print('x2', x2)
    print('x2[:2, :3]', x2[:2, :3])  # 2x3
    print('x2[:3, ::2]', x2[:3, ::2])
    print('x2[::-1, ::-1]', x2[::-1, ::-1])
    print('x2[:, 0]', x2[:, 0])  # first column of x2
    print(x2[0, :])  # first row of x2
    print(x2[0])  # equivalent to x2[0, :]
```

One important–and extremely useful–thing:

array slices is that they return *views* rather than *copies* of the array data.

list slicing in Python: in lists, slices will be copies.

explicitly copy the data within an array or a subarray  with the ``copy()`` method:
```python
x2_sub_copy = x2[:2, :2].copy()
print(x2_sub_copy)

```

#### Reshape 变形

* ndarray.reshape 数值方法
* np.newaxis     方法
* np.expand_dims 升维
* ravel（）：将多维数组拉平（一维）
* flatten（）：将多维数组拉平，并拷贝一份
* squeeze（）：除去多维数组中，维数为1的维度，如315降维后3*5
* reshape（-1）：多维数组，拉平
* reshape（-1，5），其中-1表示我们不用亲自去指定这一维度的大小，理解为n维. 变形为(*,5)

put the numbers 1 through 9 in a  3×3  grid:

```python
grid = np.arange(1, 10).reshape((3, 3))
print(grid) # [[1 2 3][4 5 6] [7 8 9]]
```

1. the size of the initial array must match the size of the reshaped array.

2. Where possible, the ``reshape`` method will use a no-copy view of the initial array, but with non-contiguous memory buffers this is not always the case.

3. Another common reshaping pattern is the conversion of a one-dimensional array into a two-dimensional row or column matrix.
   This can be done with the ``reshape`` method, or more easily done by making use of the ``newaxis`` keyword within a slice operation:

```python
x = np.array([1, 2, 3])

# row vector via reshape
x.reshape((1, 3))  # array([[1, 2, 3]])
# row vector via newaxis
x[np.newaxis, :]  # array([[1, 2, 3]])
# column vector via reshape
x.reshape((3, 1))  # array([[1],[2],[3]])
# column vector via newaxis
x[:, np.newaxis]  # array([[1],[2],[3]])
```

#### Concatenation

Concatenation, or joining of two arrays in NumPy, is primarily accomplished using the routines np.concatenate, np.vstack, and np.hstack. np.concatenate takes a tuple or list of arrays as its first argument, as we can see here:

* np.concatenate 合并 指定维度
* np.vstack  合并数组 第一维
* np.hstack 合并数组 第二维
* np.insert 插入数据

```python
    x = np.array([1, 2, 3])
    y = np.array([3, 2, 1])
    con1 = np.concatenate([x, y])
    print('concatenate([x,y])', con1)
    z = np.array([99, 99, 99])
    con2 = np.concatenate([x, y, z])
    print('concatenate([x, y, z])', con2)

    grid = np.array([[1, 2, 3],
                     [4, 5, 6]])
    con3 = np.concatenate([grid, grid])
    print('2 dims concatenate([x, y])', con3)
    con4 = np.concatenate([grid, grid], axis=1)
    print('2 dims concatenate([x, y,axis=1])', con4)

    x = np.array([9, 9, 9])
    grid = np.array([[1, 1, 1],
                     [1, 1, 1]])
    con5 = np.vstack([x, grid])
    print('mix dims vstack([x, y])', con5)
    y = np.array([[99],
                  [99]])
    con6 = np.hstack([grid, y])
    print('mix dims hstack([x, y])', con6)

```

#### Split

splitting,  is implemented by the functions np.split, np.hsplit, and np.vsplit.

```python
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    x1, x2, x3 = np.split(x, [1, 2])
    print('split', x1, x2, x3)
    grid = np.arange(16).reshape((4, 4))
    up, down = np.vsplit(grid, [2])
    print(up)
    print(down)
    left, right = np.hsplit(grid, [2])
    print(left)
    print(right)
```
