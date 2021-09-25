def bubble_sort(list_a):
  print('bubble_sort before', list_a)
  n = len(list_a)
  for k in range(n - 1):
    for i in range(n - 1 - k):
      if list_a[i] > list_a[i + 1]:
        list_a[i], list_a[i + 1] = list_a[i + 1], list_a[i]
  print('bubble_sort after', list_a)


def select_sort(list_a):
  print('select_sort before', list_a)
  n = len(list_a)
  for i in range(n - 1):
    min_index = i
    for j in range(i + 1, n):
      if list_a[min_index] > list_a[j]:
        min_index = j
    if min_index != i:
      list_a[i], list_a[min_index] = list_a[min_index], list_a[i]  # 找到最小值进行交换
  print('select_sort after', list_a)


# 插入排序， 从第2个元素开始查询，与它前面的有序列表进行比较
def insert_sort(list_a):
  print('insert_sort before', list_a)
  n = len(list_a)
  for j in range(1, n):  # 从第2个开始
    i = j
    while i > 0:
      if list_a[i] < list_a[i - 1]:
        list_a[i], list_a[i - 1] = list_a[i - 1], list_a[i]
      else:
        break
      i -= 1
  print('insert_sort after', list_a)


# 快速排序
def quick_sort(list_a, start, end):
  # 基准数
  if start >= end:
    return
  mid = list_a[start]
  low = start
  high = end  # len(list_a) - 1
  while low < high:
    # 从右到左，查询并比较 list_a[high] > mid 则 high-=1
    while low < high and list_a[high] >= mid:
      high -= 1
    list_a[low] = list_a[high]
    while low < high and list_a[low] < mid:
      low += 1
    list_a[high] = list_a[low]
  list_a[low] = mid
  quick_sort(list_a, start, low - 1)
  quick_sort(list_a, low + 1, end)


# 归并排序
def merger_sort(list_a):
  n = len(list_a)
  if n <= 1:
    return list_a
  mid = int(n / 2)
  list_left = merger_sort(list_a[0:mid])
  list_right = merger_sort(list_a[mid:n])
  # 对 list_left / list_right进行合并
  result = [] # 接收合并的数组
  i_left,i_right =0,0
  while i_left < len(list_left) and i_right < len(list_right):
    if list_left[i_left] < list_right[i_right]:
      result.append(list_left[i_left])
      i_left += 1
    else:
      result.append(list_right[i_right])
      i_right += 1
  # 退出循环, 是否有剩余的
  result += list_left[i_left:] # result.extend() 列表相加  extend比+=快
  result += list_right[i_right:]
  return result

