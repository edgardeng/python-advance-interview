'''
'  写入操作
'''
f = open('a.txt', 'a')
a = 'content\n'
f.write(a)
f.close()


'''
使用with 不用 close
'''
