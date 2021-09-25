# 顺序查找
def sequence_search(list_a, v):
  for i in list_a:
    if v == list_a[i]:
      return i
  return -1


# 二分查找
def binary_search(list_a, v):
  n = len(list_a)
  start = 0
  end = n - 1
  while start <= end:
    mid = int((start + end) / 2)
    if list_a[mid] == v:
      return mid
    elif list_a[mid] > v:
      end = mid - 1
    else:
      start = mid + 1
  return -1


# 二分查找 递归 前提是已排序的
def binary_search2(list_a, v):
  n = len(list_a)
  print(list_a)
  if n < 1:
    return -1
  start = 0
  end = n - 1
  mid = int((start + end) / 2)
  if list_a[mid] == v:
    return mid
  elif list_a[mid] > v:
    return binary_search2(list_a[start: mid - 1], v)
  else:
    return binary_search2(list_a[mid + 1:end], v)
