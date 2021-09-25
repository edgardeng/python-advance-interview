'''
'  基本的try /except 控制语句
'''

try:
  a = 4 / 0
except BaseException as e:
  print(e)

'''
'  多个try /except 控制语句
'  异常: 先子类，后父类
'''

try:
  a = '1' # input('输入被除数')
  b = '0' # input('输入除数')
  c = float(a) / float(b)
except ZeroDivisionError as e1:
  print('除数不能为0')
except BaseException as e3:
  print('出错了', e3)
else:
  print('结果', c)
finally:
  print('您的输入:', a, '/', b)

'''
'  with 上下文管理语法结构
'  （在代码块执行完毕后自动还原进入该代码之前的现场和上下文）
'   常用在 文件操作和 网络通讯
'''

# with open('a.txt') as text_file:
#   content = text_file.readline()
#   print(content)

import traceback
try:
  n = 1/ 0
except:
  traceback.print_exc()
  # 使用traceback打印报错信息

'''
'  自定义异常
'''
class AgeError(Exception):
  def __init__(self, info):
    Exception.__init__(self)
    self.errorInfo = info
  def __str__(self):
    return str(self.errorInfo)+ '!,年龄错误'

age = int(input('请输入'))
if age < 1 or age > 100:
  raise AgeError(age)
else:
  print('年龄',age)
