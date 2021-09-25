## Seaborn

> Seaborn是基于matplotlib的图形可视化python包。它提供了一种高度交互式界面，便于用户能够做出各种有吸引力的统计图表。

Seaborn视为matplotlib的补充，而不是替代物。同时它能高度兼容numpy与pandas数据结构以及scipy与statsmodels等统计模式。

### 安装
```
python3 -m pip install --upgrade pip
pip3 install seaborn -U
```
### seaborn API
 
Seaborn 要求原始数据的输入类型为 pandas 的 Dataframe 或 Numpy 数组，画图函数有以下几种形式:

* sns.图名(x='X轴 列名', y='Y轴 列名', data=原始数据df对象)

* sns.图名(x='X轴 列名', y='Y轴 列名', hue='分组绘图参数', data=原始数据df对象)

* sns.图名(x=np.array, y=np.array[, ...])

#### 直方图的绘制 barplot

将点估计和置信区间显示为矩形条。

条形图表示具有每个矩形的高度的数值变量的集中趋势的估计，并且使用误差条提供围绕该估计的不确定性的一些指示

API介绍

seaborn.barplot(x=None, y=None, hue=None, data=None, order=None, hue_order=None, estimator=<function mean>, ci=95, n_boot=1000, units=None, orient=None, color=None, palette=None, saturation=0.75, errcolor='.26', errwidth=None, capsize=None, dodge=True, ax=None, **kwargs)
Example for barplot
```python
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

x = np.arange(8)
y = np.array([1,5,3,6,2,4,5,6])

df = pd.DataFrame({"x-axis": x,"y-axis": y})

sns.barplot("x-axis","y-axis",palette="RdBu_r",data=df)
plt.xticks(rotation=90)
plt.show()

```

### 5 种主题风格
* darkgrid
* whitegrid
* dark
* white
* ticks


```

```


despine 自定义风格


set_context 


### 颜色 与 调色板

color_palette 传入任何matplotlib 支持的颜色
color_palette 不传参数，默认颜色
set_palette 设置所有图的颜色

分类色板

10 个默认颜色： deep, muted, pastel, bright

使用圆形画板：
 * 使用hls颜色空间    `sns.palplot(sns.color_palette('hls',8))`
 * 使用hls_palette   `sns.palplot(sns.hls_palette(8,l=.7,s=.9))`
 * 使用对比          `sns.palplot(sns.color_palette('Paried',8))`
 * 使用xkcd随机颜色     `colors = ['windows blue'] sns.palplot(sns.xkcd_palette(colors)`
 * 连续色板         `sns.palplot(sns.color_palette('Blues'))` 或 `sns.palplot(sns.color_palette('BuGn_r'))` 使用_r后缀，颜色有深到浅
 * 线性变化     `sns.palplot(sns.color_palette('cubehelix',8))` 或   `sns.palplot(sns.cubehelix_palette(8,start=.5,rot=.5))`
 * 连续调色     `sns.palplot(sns.light_palette('grren'))` 浅到深的绿色 或 `sns.palplot(sns.dark_palette('purple'))` 深到浅的紫 也可以使用reverse参数进行反转
 
### 单变量

### 回归分析绘图

### 对类别值的绘图


factorplot 函数的使用
* x,y,hue   数据集的变量名
* data  数据集的数据
* row,col   分类变量进行平铺显示、变量名
* col_wrap  每行最高平铺数

### 多子图的绘图

#### FaceGrid 展示子图

#### PairGrid 展示子图
