'''
集合

常用的模块

  builtins


'''

var = {} # dict
var2 = {1,2,3,4} # set
print(var)
print(var2)

var3 = {3,6,5,4}
print(var2 & var3) # 交集
print(var2 | var3) # 并集
print(var2 ^ var3) # 并集 - 交集
print(var2 - var3) # 差集
print(var3 - var2) # 差集

# append extend insert
var2.add(4)
var2.add(40)
var2.remove(2)  # 按值添加，按值删除，没有索引
print(var2)





