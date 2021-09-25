'''
' 加密
'''
from hashlib import  *


'''
' MD5 （不可逆）
'''
if __name__ == '__main__':

  m = md5()
  password = '123456'
  print(password.encode())
  m.update(password.encode())

  m.update(''.encode())


  print(m.hexdigest())
