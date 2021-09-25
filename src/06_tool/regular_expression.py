'''
'  Python Regular Expression 正则表达式
'
'''
import re


def test_match():
  s = 'hello python Hello'
  p = 'hello'
  o = re.match(p, s)
  print(o)
  print(dir(o))
  print(o.group())  # 返回匹配的字符串
  print(o.span())  # 范围
  print(o.start())  # 开始处
  print('*' * 30, 'flags参数的使用')
  o2 = re.match(p, s, re.L)
  print(o2.group())  # 返回匹配的字符串


# 常用字符的使用
def test_match_character():
  print('-' * 30, ' . 匹配任意一个字符')
  print(re.match('.', 'abv'))
  print(re.match('.', '12'))
  print(re.match('.', '\n'))

  print('-' * 30, ' \d 匹配数字 0-9')
  print(re.match('\d', 'abc456'))
  print(re.match('\d', '234svd'))

  print('-' * 30, ' \D 匹配非数字 0-9')
  print(re.match('\D', 'abc456'))
  print(re.match('\D', '234svd'))

  print('-' * 30, ' \s 匹配空白字符')
  print(re.match('\s', '\n12\t'))
  print(re.match('\s', '\t'))
  print(re.match('\s', 'addd'))

  print('-' * 30, ' \S 匹配非空白字符')
  print(re.match('\S', '\n12\t'))
  print(re.match('\S', '\t'))
  print(re.match('\S', 'addd'))

  print('-' * 30, ' \w 匹配字母、数字')
  print(re.match('\w', 'AB'))
  print(re.match('\w', 'ab'))
  print(re.match('\w', '12'))
  print(re.match('\w', '__'))
  print(re.match('\w', '##'))

  print('-' * 30, ' \W 匹配非 字母、数字')
  print(re.match('\W', 'AB'))
  print(re.match('\W', 'ab'))
  print(re.match('\W', '12'))
  print(re.match('\W', '__'))
  print(re.match('\W', '##'))

  print('-' * 30, ' \[] 匹配列表中的字符')
  print(re.match('[2468]', '22'))
  print(re.match('[2468]', '33'))
  print(re.match('[2468]', '83'))
  print(re.match('[2468]', '38'))


def test_match_phone():
  print('-' * 30, ' 匹配手机号')
  patten = '\d\d\d\d\d\d\d\d\d\d\d'
  print(re.match(patten, '13466669999'))
  print(re.match('1[345789]\d\d\d\d\d\d\d\d\d', '13466669999'))


# 限定符
def test_match_qualifier():
  print('-' * 30, ' * 匹配零次或多次')
  print(re.match('\d*', '123abc'))  # 匹配开头的数字
  print(re.match('\d*', 'abc'))
  print('-' * 30, ' + |匹配一次或多次')
  print(re.match('\d+', '123abc'))  # 匹配开头的数字
  print(re.match('\d+', 'abc'))
  print('-' * 30, ' ？ |匹配一次或零次')
  print(re.match('\d?', '1abc'))
  print(re.match('\d?', '123abc'))  # 匹配开头的数字
  print(re.match('\d?', 'abc'))

  print('-' * 30, ' {m} |重复m次')
  print(re.match('\d{2}', '123abc'))  # 匹配开头2个数字
  print(re.match('\d{2}', '12abc'))
  print(re.match('\d{2}', '1abc'))
  print(re.match('\d{2}', 'abc'))

  print('-' * 30, '{m,n}|重复m到n次')
  print(re.match('\d{1,3}', '1234abc'))  # 匹配开头2个数字
  print(re.match('\d{1,3}', '123abc'))
  print(re.match('\d{1,3}', '12abc'))
  print(re.match('\d{1,3}', '1abc'))
  print(re.match('\d{1,3}', 'abc'))

  print('-' * 30, '{m,}|至少m次')
  print(re.match('\d{2,}', '1234abc'))  # 匹配开头2个数字
  print(re.match('\d{2,}', '123abc'))
  print(re.match('\d{2,}', '12abc'))
  print(re.match('\d{2,}', '1abc'))
  print(re.match('\d{2,}', 'abc'))

  print('-' * 30, '案例1 首字母为大写字符，其他小写字符')
  print(re.match('[A-Z][a-z]*', 'abc'))
  print(re.match('[A-Z][a-z]*', 'ABC'))
  print(re.match('[A-Z][a-z]*', 'Abc'))
  print(re.match('[A-Z][a-z]*', 'AbC'))
  print('-' * 30, '案例2 有效变量名 字母数字下划线，数字不开头')
  print(re.match('[a-zA-Z_][a-zA-Z0-9_]*', 'abc'))
  print(re.match('[a-zA-Z_]\w*', 'abc'))
  print(re.match('[a-zA-Z_][a-zA-Z0-9_]*', 'abc123'))
  print(re.match('[a-zA-Z_]\w*', '123abc'))
  print(re.match('[a-zA-Z_]\w*', '_123abc'))

  print('-' * 30, '案例2 1-99的数字')
  print(re.match('[1-9]\d?', '23abc'))
  print(re.match('[1-9]\d?', '100'))
  print(re.match('[1-9]\d?', '11'))
  print(re.match('[1-9]\d?', '1'))
  print(re.match('[1-9]\d?', '0'))
  print(re.match('[1-9]\d?', '09'))
  print('-' * 30, '案例2 8-20随机密码  大写，小写，下划线，数字')
  print(re.match('\w{8,20}', '1234567'))
  print(re.match('\w{8,20}', '1234567$$'))
  print(re.match('\w{8,20}', '1234567abc_'))
  print(re.match('\w{8,20}', '1234567abc#'))
  print(re.match('\w{8,20}', '12345678901234567890zx'))


# 转义字符 原生字符
def escape_character():
  print('C:\t\d\e')
  print('C:\\t\\d\\e')
  print(r'C:\t\d\e')


# 边界字符
def boundary():
  print('-' * 30, '$ 匹配字符串结尾')
  print(re.match('[1-9]\d{4,9}@qq.com', '1234567@qq.com'))
  print(re.match('[1-9]\d{4,9}@qq.com', '1234567@qq.com.126.cn'))
  print(re.match(r'[1-9]\d{4,9}@qq.com$', '1234567@qq.com'))
  print(re.match(r'[1-9]\d{4,9}@qq.com$', '1234567@qq.com.126.cn'))
  print('-' * 30, ' ^ 匹配字符串开头')
  print(re.match(r'^hello.*', 'hello abc'))
  print(re.match(r'^hello.*', 'abc hello abc'))
  print('-' * 30, ' \b 匹配单词的边界')
  print(re.match(r'.*\bab', '123 aabc'))  # 单词 ab 开始
  print(re.match(r'.*\bab', '123 abcd'))
  print(re.match(r'.*\bab', '123 aaa'))
  print(re.match(r'.*\bab', '123 abcd cdab'))
  print(re.match(r'.*ab\b', '123 abc'))  # 单词 ab 结尾
  print(re.match(r'.*ab\b', '123 aaa'))
  print(re.match(r'.*ab\b', '123 ab'))
  print(re.match(r'.*ab\b', '123 cdab'))
  print(re.match(r'.*ab\b', '123 abcd cdab'))


def test_search():
  print(re.match(r'hello', 'hello python'))
  print(re.search(r'hello', 'hello python'))
  print(re.match(r'hello', 'python hello'))
  print(re.search(r'hello', 'python hello '))
  print(re.match('aa|bb|cc', 'aa'))
  print(re.match('aa|bb|cc', 'bbb'))
  print(re.match('aa|bb|cc', 'ccc'))
  print(re.match('aa|bb|cc', 'a bb ccc'))
  print(re.search('aa|bb|cc', 'a bb ccc'))


# 多个字符
def test_multi_character():
  print('-' * 30, '案例 0-100之间的数字: 0-99 | 100')
  print(re.match('[1-9]?\d|100', '1'))
  print(re.match('[1-9]?\d|100', '11'))
  print(re.match('[1-9]?\d|100', '100'))
  print(re.match('[1-9]?\d$|100$', '100'))
  print(re.match('[1-9]?\d$|100$', '1000'))
  print('-' * 30, '案例 ')
  print(re.match('[ab][cd]', 'ab'))
  print(re.match('[ab][cd]', 'ac'))
  print(re.match('[ab][cd]', 'ad'))
  print(re.match('ab|cd', 'abc'))
  print(re.match('ab|cd', 'ac'))


# 匹配分组
def test_group():
  print('-' * 30, '座机号码 区号{3,4} 号码{5,8}  010-0000 0791-222222')
  print(re.match(r'\d{3,4}-[1-9]\d{4,7}', '010-10086'))
  print(re.match(r'\d{3,4}-[1-9]\d{4,7}', '010-88888888'))
  print(re.match(r'\d{3,4}-[1-9]\d{4,7}', '1111-10086'))
  print(re.match(r'\d{3,4}-[1-9]\d{4,7}', '1111-88888888'))

  print('-' * 30, ' 匹配分组')
  o = re.match(r'(\d{3,4})-([1-9]\d{4,7})', '1111-88888888')
  print(o)
  print(o.group(0), o.group(1), o.group(2))
  print(o.groups(), o.groups()[0], o.groups()[1])
  print('-' * 30, 'html 标签')
  print(re.match(r'<.+><.+>.+</.+></.+>', '<html><a>abc</a></html>'))
  print(re.match(r'<.+><.+>.+</.+></.+>', '<html><a>abc</b></html>'))
  print(re.match(r'<(.*)><(.*)>.*</\2></\1>', '<html><a>abc</b></html>'))
  print(re.match(r'<(.*)><(.*)>.*</\2></\1>', '<html><d>abc</d></html>'))
  print('-' * 30, 'html 标签 - 别名')
  print(re.match(r'<(?P<k_html>.+)><(?P<k_head>.+)>.*</(?P=k_head)></(?P=k_html)>', '<html><d>abc</d></html>'))


## 搜索与替换
def test_sub():
  print('-' * 30, ' 替换')
  print(re.sub(r'#.*$', '', '2004-222-23322 # 这是个什么'))  # 替换#开头的部分
  print(re.sub(r'#\D*', '', '2004-222-23322 # 这是个什么'))
  print('-' * 30, ' 替换 subn')
  print(re.subn(r'#\D*', '', '2004-222-23322 # 这是个什么'))
  print(re.subn(r'#.*$', '', '2004-222-23322 # 这是个什么'))


def test_compile():
  print('-' * 30, ' compile的使用')
  regex = re.compile(r'\w+')  # 匹配字母或数字
  print(regex.match('1223dfdf'))
  print(regex.match('##1223dfdf'))


def test_findall():
  print('-' * 30, ' findall 返回数组')
  print(re.findall(r'\w', '##1223dfdf'))  # 匹配字母或数字 f
  print(re.findall(r'\w+', '## 1223 df df 1'))
  print('-' * 30, ' finditer 返回迭代器')
  print(re.finditer(r'\w+', '## 1223 df df 1'))
  for i in re.finditer(r'\w+', '## 1223 df df 1'):
    print(i, i.group())


def test_split():
  print('-' * 30, ' split 返回数组')
  print(re.split(r'\d+', '123abc123abc'))
  print(re.split(r'\d+', '123 abc 123 abc'))
  print(re.split(r'\d+', 'abc123 abc 123 abc'))
  print(re.split(r'\d+', 'abc 123 abc 123 abc',1))

def greedy_mode():
  print('-' * 30, ' 贪婪模式')
  result = re.match(r'(.+)(\d+-\d+-\d+)', 'this is my tel: 122-1244-1242')
  print(result.group(1))
  print(result.group(2))
  print('-' * 30, ' 非贪婪模式 尽可能少的匹配')
  result = re.match(r'(.+?)(\d+-\d+-\d+)', 'this is my tel: 122-1244-1242')
  print(result.group(1))
  print(result.group(2))

  print('-' * 30, ' 贪婪模式')
  print(re.match(r'abc(\d+)', 'abc123456'))
  print(re.match(r'abc(\d+?)', 'abc123456'))


if __name__ == '__main__':
  # test_match()
  # test_match_character()
  # test_match_phone()
  # test_match_qualifier()
  # escape_character()
  # boundary()
  # test_search()
  # test_multi_character()
  # test_group()
  # test_sub()
  # test_compile()
  # test_findall()
  # test_split()
  # greedy_mode()
# <.+><.+>.+</.+></.+>
  s = '<link href="../assets/css/app.css?t=20112455" type="text/css" rel="stylesheet">'
  mathched = re.findall(r'\S+assets/css/\S+.css\S+"', s)
  for m in mathched:
    print(m, m.index('.css'))
    s = s.replace(m, m[:m.index('.css')] + '.css?t=00000"')
  print(s)
