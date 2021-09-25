import time
from sort_algorithm import bubble_sort, select_sort, insert_sort, quick_sort, merger_sort
from search_algorithm import sequence_search, binary_search, binary_search2

# 题目1, 如果a+b+c =1000,a*a + b*b =c*c,(abc为自然数)，求出abc的组合
def a_b_c():
  start_at = time.time()
  for a in range(1001):
    for b in range(1001):
      for c in range(1001):
        if a + b + c == 1000 and a ** 2 + b ** 2 == c ** 2:
          print('a=%d,b=%d,c=%d' % (a, b, c))
  print('use ', time.time() - start_at)  # 最笨的方法 穷举


def a_b_c2():
  start_at = time.time()
  for a in range(1001):
    for b in range(1001):
      c = 1000 - a - b
      if a ** 2 + b ** 2 == c ** 2:
        print('a=%d,b=%d,c=%d' % (a, b, c))
  print('use ', time.time() - start_at)  # 最笨的方法 穷举


if __name__ == '__main__':
  # a_b_c2()
  list_a = [2, 5, 3, 4, 10, 1, 7, 9, 6, 8, 0]
  # list_a.insert(99, 99)
  # print('before', list_a[2:-9])
  # bubble_sort(list_a)
  # select_sort(list_a)
  # insert_sort(list_a)
  print('before', list_a)
  # quick_sort_reverse(list_a, 0, len(list_a) - 1)
  list_a = merger_sort(list_a)
  print('after', list_a)
  # index = sequence_search(list_a, 99)
  index = binary_search2([2], 1)
  print('find', index if index > -1 else 'none')
