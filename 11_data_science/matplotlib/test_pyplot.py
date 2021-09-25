import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False


def make_a_figure():
  data = np.arange(10)
  p = plt.figure(figsize=(8, 6))
  plt.title('line')
  plt.xlabel('X')
  plt.xlabel('Y')
  plt.xlim(0, 5)
  plt.ylim(0, 100)
  plt.xticks(range(0, 12, 2))
  plt.yticks(range(0, 120, 20))
  plt.plot(data, data)  # y=x
  plt.plot(data, data ** 2)  # y=x*x

  plt.plot([2], [4], 'o')
  plt.annotate('(2,4)', xy=(2, 4), xytext=(2, 4),)
  if not os.path.exists('pic'):
    os.mkdir('pic')
  plt.savefig('pic/line.png')
  plt.show()

  if not os.path.exists('pic'):
    os.mkdir('pic')
  plt.savefig('pic/line.png')
  plt.show()


def make_sub_figure():
  data = np.arange(0, np.pi * 2, 0.01)
  p = plt.figure(figsize=(8, 6))  # 画布大小
  sub1 = p.add_subplot(2, 1, 1)
  plt.title('line')
  plt.xlabel('X')
  plt.xlabel('Y')
  plt.xlim(0, 1)
  plt.ylim(0, 1)
  plt.xticks(np.arange(0, 1.2, 0.2))
  plt.yticks(np.arange(0, 1.2, 0.2))
  plt.plot(data, data ** 2)
  plt.plot(data, data ** 4)
  plt.legend(['y=x^2', 'y=x^4'])
  sub1 = p.add_subplot(2, 1, 2)
  plt.title('sin/cos')
  plt.xlabel('rad')
  plt.xlabel('value')
  plt.xlim(0, np.pi * 2)
  plt.ylim(-1, 1)
  plt.xticks(np.arange(0, np.pi * 2.5, np.pi * 0.5))
  plt.yticks(np.arange(-1, 1.5, 0.5))
  plt.plot(data, np.sin(data))
  plt.plot(data, np.cos(data))
  plt.legend(['sin', 'cos'])
  plt.show()


def make_a_bar():
  week = np.array(['周一', '周二', '周三', '周四', '周五', '周六', '周七'])
  total = np.random.randint(1000, 5000, size=7)
  color = np.random.rand(15).reshape(5, 3)
  p = plt.figure(figsize=(8, 6))
  sub1 = p.add_subplot(2, 1, 1)
  plt.bar(week, total, color=color)
  sub2 = p.add_subplot(2, 1, 2)
  plt.barh(week, total, color=color)
  plt.show()

def make_a_hist():
  x = [np.random.randint(0, n, n) for n in [3000, 4000, 5000]]
  bins = [0, 100, 500, 1000, 2000, 3000, 4000, 5000]
  labels = ['3k', '4k', '5k']
  plt.hist(x, bins=bins, label=labels)
  plt.legend()
  plt.show()


def make_a_pie():
  data = np.array([6, 1, 2])
  # data = np.array([0.6, 0.1, 0.2])
  pet = ['Dog', 'Cat', 'Pig']
  # plt.pie(data, labels=pet, autopct='%1.2f%%', colors=['red', 'yellow', 'green'])
  plt.pie(data, labels=pet, autopct='%1.2f%%', colors=['red', 'yellow', 'green'],
          labeldistance=1.2, pctdistance=0.5,
          explode=[0.1, 0.1, 0.1],
          shadow=True, startangle=90)
  plt.legend()
  plt.show()


def make_a_scatter():
  x = np.random.randn(1000)
  y = np.random.randn(1000)
  color = np.random.rand(3000).reshape(1000, 3)
  size = np.random.randint(0, 100, 1000)  # 设置大小
  plt.scatter(x, y, color=color, s=size, alpha=0.5)
  plt.show()


def make_a_box():
  data = np.random.randint(90, 150, 15).reshape(5, 3)
  labels = ['2018', '2019', '2020']
  plt.title('1-5年级总人口')
  plt.boxplot(data, notch=True, labels=labels, meanline=True)
  plt.show()


if __name__ == '__main__':
  make_a_figure()
  # makae_sub_figure()
  # make_a_bar()
  # make_a_hist()
  # make_a_pie()
  # make_a_scatter()
  # make_a_box()
