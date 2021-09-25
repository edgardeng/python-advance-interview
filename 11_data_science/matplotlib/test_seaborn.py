import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import scipy.stats as stats


def sin_plot(flip=1):
  sns.set()
  x = np.linspace(0, 14, 100)
  for i in range(1, 7):
    plt.plot(x, np.sin(x + i * 0.5) * (7 - i) * flip)  # 绘制6条sin线
  plt.show()


def test_style():
  sns.set_style('whitegrid')
  sns.despine(offset=10)
  # sns.despine()
  sns.boxplot(data=np.random.normal(size=(20, 6)), palette=sns.color_palette('hls', 8))
  plt.show()


def test_color():
  # 查看默认的颜色空间
  current_plt = sns.color_palette()
  sns.palplot(current_plt)
  # 设置指定的画板
  sns.palplot(sns.color_palette('hls', 8))
  plt.show()


def test_dark_palette():
  x, y = np.random.multivariate_normal([0, 0], [[1, -.5], [-.5, 1]], size=300).T
  pal = sns.dark_palette('green', as_cmap=True)
  sns.kdeplot(x, y, cmap=pal)
  # sns.palplot(sns.light_palette(210,90,60),input='hus1')


def single_variable():
  # x = np.random.normal(size=100)
  # sns.distplot(x,kde=False) # 最基本的分布 kde和密度估计
  # sns.distplot(x,bins=20, kde=False)

  x = np.random.gamma(6, size=200)
  sns.distplot(x, bins=20, kde=False, fit=stats.gamma)

  plt.show()


def single_variable_scatter():
  mean, cov = [0, 1], [(1, 0.5), (0.5, 1)]  # 均值，协方差
  data = np.random.multivariate_normal(mean, cov, 500)
  df = pd.DataFrame(data, columns=['x', 'y'])
  print(df.head())
  # 2 个变量之间的分布关系，最后的是散点图
  # sns.jointplot(x='x',y='y',data=df)

  # 使用黑白色加深颜色
  with sns.axes_style('white'):
    sns.jointplot(x='x', y='y', data=df, kind='hex', color='k')

  plt.show()


def seaborn_pairplot():
  iris = sns.load_dataset('iris')  # 加载数据集
  sns.palplot(iris)
  plt.show()


# 使用regplot mplot 绘制回归关系， 推荐regplot
def seaborn_regplo():
  np.random.seed(sum(map(ord, 'regression')))
  tips = sns.load_dataset('tips')
  tips.head()
  sns.regplot(x='total_bill', y='tip', data=tips)  # 总费用和小费的关系
  # sns.regplot(x='size', y='tip', data = tips) #
  sns.regplot(x='total_bill', y='tip', data=tips, x_jitter=0.05)  # 使用 x_jitter添加抖动

  plt.show()


def seaborn_stipplot():
  np.random.seed(sum(map(ord, 'categorical')))
  titanic = sns.load_dataset('titanic')
  titanic.head()
  tips = sns.load_dataset('tips')
  iris = sns.load_dataset('iris')

  sns.stripplot(x='day', y='total_bill', data=tips)
  sns.stripplot(x='day', y='total_bill', data=tips, jitter=True)  # 存在重叠时，进行左右偏移
  sns.swarmplot(x='day', y='total_bill', data=tips)  # 树型
  sns.swarmplot(x='day', y='total_bill', data=tips, hue='sex')  #
  sns.swarmplot(x='day', y='total_bill', data=tips, hue='time')  # 使用颜色标记第2个变量
  # 箱线图
  sns.boxplot(x='day', y='total_bill', data=tips, hue='time')
  # 小提琴 图
  sns.violinplot(x='total_bill', y='day', data=tips, hue='time')
  sns.violinplot(x='day', y='total_bill', data=tips, hue='sex', split=True)  # 使用split 左右分开某个变量

  sns.barplot(x='sex', y='survived', hue='class', data=titanic)  # 不同仓位，不同性别的获救率
  # 点图更好的描述变化的差异
  sns.pointplot(x='sex', y='survived', hue='class', data=titanic)
  sns.pointplot(x='class', y='survived', hue='sex', data=titanic,
                palette={'male': 'g', 'female': 'm'},
                markers=['.', 'o'], linestyles=['-', '--'])
  # 宽型数据 使用箱线图
  sns.boxplot(data=iris, orient='h')

  # 多层面板分类图
  sns.factorplot(x='day', y='total_bill', data=tips, hue='smoker')  # 默认折线图
  sns.factorplot(x='day', y='total_bill', data=tips, hue='smoker', col='time', kind='swarm')
  sns.factorplot(x='day', y='total_bill', data=tips, hue='smoker', col='time', kind='box', size=4, aspect=.5)


def test_facegrid():
  np.random.seed(sum(map(ord, 'axis_grids')))
  tips = sns.load_dataset('tips')
  tips.head()
  g = sns.FacetGrid(tips, col='time')  #
  g.map(plt.hist, 'tip')  # 指定图

  # 散点图
  g = sns.FacetGrid(tips, col='sex', hue='smoker')  #
  g.map(plt.scatter, 'total_bill', 'tip', alpha=.7)
  g.add_legend()

  # 回归图
  g = sns.FacetGrid(tips, col='time', row='smoker', margin_titles=True)
  g.map(sns.regplot, 'size', 'total_bill', color='.1', fit_reg=True, x_jitter=.1)  # fit_reg是否显示回归线

  # 布局参数
  g = sns.FacetGrid(tips, col='day', size=4, aspect=.5)  # 长宽比，大小
  g.map(sns.barplot, 'sex', 'total_bill')

  # 类别展示顺序
  ordered_days = tips.day.value_counts().index
  print(ordered_days)
  ordered_days = pd.Categorical(['Thur', 'Fri', 'Sat', 'Sun'])
  g = sns.FacetGrid(tips, row='day', row_order=ordered_days, size=7, aspect=4)  # 长宽比，大小
  g.map(sns.boxplot, 'total_bill')

  # 散点图的大小
  pal = {'Lunch': 'seagreen', 'Dinner': 'gray'}
  g = sns.FacetGrid(tips, hue='time', palette=pal, size=5)  # hue_kws={'marker':['o','v']} 指定形状
  g.map(sns.scatterplot, 'total_bill', 'tip', s=50, alpha=.7, linewidth=.5, edgecolor='white')  # s 点的大小
  g.add_legend()

  # label的使用
  with sns.axes_style('white'):
    g = sns.FacetGrid(tips, row='sex', col='smoker', margin_titles=True, size=2.5)
  g.map(plt.scatter, 'total_bill', 'tip', color='#334488', edgecolor='white', lw=0.5)
  g.set_axis_labels('Total Bill', 'Tip')  # 设置label 坐标轴的标签
  g.set(xticks=[10, 30, 50], yticks=[2, 6, 10])
  g.fig.subplots_adjust(wspace=.02, hspace=.02)
  g.fig.subplots_adjust(left=0.1, right=0.6, bottom=0.1, top=0.9, wspace=.02, hspace=.02)


def test_pairgrid():
  # iris = sns.load_dataset('iris')
  iris = pd.read_csv('../data/iris.csv')

  # g = sns.PairGrid(iris)
  # g.map(plt.scatter) # 两两变量去画散点图

  g = sns.PairGrid(iris)
  g.map_diag(plt.hist)  # 对角线的子图画直方图
  g.map_offdiag(plt.scatter)  # 非对角线的子图画散点图

  g = sns.PairGrid(iris, hue='species')  # 添加一个变量 species
  g.map_diag(plt.hist)  # 对角线的子图画直方图
  g.map_offdiag(plt.scatter)  # 非对角线的子图画散点图
  g.add_legend()

  g = sns.PairGrid(iris, vars=['sepal_length', 'sepal_width'], hue='species')  # 通过vars指定需要画图的变量  palette='GnBu_d' 设置调色板
  g.map(plt.scatter)  # s=20 设置圆点大小, edgecolor设置边界颜色

  plt.show()


def test_heatmap():
  # 简单的热力图
  data = np.random.rand(3, 3)
  # heatmap = sns.heatmap(data)
  # heatmap = sns.heatmap(data, vmin=0.2, vmax=0.5) # 设置最大，最小取值

  data = np.random.randn(3, 3)  #
  # heatmap = sns.heatmap(data, center=0) # 设置中间值 0
  # flights = sns.load_dataset('flights')
  flights = pd.read_csv('../data/flights.csv')
  flights_data = flights.pivot('month', 'year', 'passengers')
  # heatmap = sns.heatmap(flights_data)
  heatmap = sns.heatmap(flights_data, annot=True, fmt='d', linewidth=5, cmap='YlGnBu')  # 使用annot设显示数值， 使用linewidth=5 添加间距, 使用cmap设置颜色条
  # 使用 cbar=False 隐藏颜色条

  #特征与特征的相关性 使用 热力图

  plt.show()


if __name__ == '__main__':
  #  # 添加 set() 有前后风格变化
  # sin_plot()
  # test_style()
  # test_dark_palette()
  # single_variable()
  # single_variable_scatter()
  # seaborn_pairplot()
  # test_facegrid()
  # test_pairgrid()
  test_heatmap()
