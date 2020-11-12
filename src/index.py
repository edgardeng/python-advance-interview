# def func_a(a, b=1):
#     print(a, b)
# func_a(1),func_a(1,2),func_a(1,b=2)

# def func_a(a, b=1, *args, **kwargs):
#     print('+' * 20)
#     print(a, b)
#     print('-' * 10)
#     print(args)
#     print(kwargs)
# func_a(1, 2, 3, k=4, j=5) 可用
# func_a(1, b=2, k=4, j=5)  可用
# func_a(1, b=2, 3, k=4, j=5)  不可用

# def func_a(a, *args, b=2, **kwargs):
#     print('+' * 20)
#     print(a, b)
#     print('-' * 10)
#     print(args)
#     print(kwargs)
#     func_a(1, 0, 3, k=4, j=5) # 可以
#     func_a(1, 0,0,0,  k=4, j=5,b=3)# 可以 参数b重复了
#     func_a(1,b=2,3) # 不可以

# def func_a(a, **kwargs, *args): # 不可定义

def func_a(a=1, b=2, *args, **kwargs):
    print('+' * 20)
    print(a, b)
    print('-' * 10)
    print(args)
    print(kwargs)
    # func_a(a=1,b=2, c=3) # 可用
    # func_a(0, 1, 2, 3)# 可用
    # func_a(0, k=4, j=5,b=2)# 可用
    # func_a(0, 1, 2, 3, 4, k=4, j=5)# 可用
#     func_a(1, 0,0,0,  k=4, j=5,b=3) 不可参数b重复了
#     func_a(a=1,2,c=3) 不可以
#     func_a(a=1,b=2,4,c=3)  # 不可以 位置参数不能在关键字参数后面

# def func_a(a=1,b=2, c, *args): # 不可定义 位置参数不能在关键字参数后面

# def func_a(a, b, *args, c, **kwargs):  # 可定义 不可用 missing 1 required keyword-only argument: 'c'

def f1(a, b, c=0, *args, **kw):
    print('a =', a, 'b =', b, 'c =', c, 'args =', args, 'kw =', kw)

if __name__ == '__main__':
    a = [2]
    b = [99, 100]
    print(id(a))
    print(id(b))
    # a[:] = b # [99,100]
    a = [99,100]
    print(id(a))
    print(id(b))
    # f1(1, 2, 3 , x=4, y=5,c=99)
    # func_a(a=1,b=2, c=3)
    # func_a(0, 1, 2, 3)
    # func_a(0, k=4, j=5,b=2)
    # func_a(0, 1, 2, 3, 4, k=4, j=5)
    # # func_a(1, 0, 3, k=4, j=5)
    # # func_a(1, 0,0,0,  k=4, j=5,b=3)
    # # func_a(1,b=2)
    #
    # a = len('中'.encode())
    # print(a)
    #
    # dic = {}
    # d = {'b': 'c', 'c': 'd'}
    # dic['a'] = d
    #
    # dic['b'] = dic['a']
    #
    # dic['b']['c'] = 'dddd'
    # print(dic)
    # del dic['a']
    # print(dic)


    # print(add_end([1, 2, 3]))
    # print(add_end())
    # print(add_end())

