# Matplotlib

> matplotlib 最流行的python底层绘图库

* 各种高硬拷贝格式和跨平台的交互式环境，生成用于出版质量级别的图形
* 操作简单
* 提供pylab的模块，方便用户快速计算和绘图

 
## pyplot的使用

使用 pyplot.plot绘制简单的图形 

```
import matplotlib.pyplot as plt
import numpy as np
plt.plot(np.random.randn(100))
plt.show() # 展示
```

### 使用pyplot绘图步骤

1. 创建画布 plt.figure 
    > 参数： num=None,  图像编号
            figsize=None,  # defaults to rc figure.figsize 宽高元组
            dpi=None,  # defaults to rc figure.dpi 分辨率（每英寸多少个像素，默认80）
            facecolor=None,  # defaults to rc figure.facecolor 背景颜色
            edgecolor=None,  # defaults to rc figure.edgecolor 边框颜色
            frameon=True, 是否显示边框
           
2. 创建子图 figure.add_subplot
    > nrows 子图的总行数,ncols 子图的纵列数,index 子图的位置

3. 添加画布内容
    > plt.title       添加标题
      plt.xlabel      添加x轴名称
      plt.ylabel      添加y轴名称
      plt.xlim         x轴的范围
      plt.ylim            y轴的范围
      plt.xticks          x轴刻度的数目与取值
      plt.yticks          y轴刻度的数目与取值
      plt.legend          图例

4. 绘制图形 plt.plot
    > 参数 x轴数据，y轴数据，format_string控制曲线的格式字符串

5. 保存图形 plt.savefig
    > 参数： fname 文件路径 dpi 图像分辨率 facecolor，edgecolor， format: jpg,png,pdf,svg ,bbox_inches 保存部分。如果tight 会裁剪空白部分

6. 显示图形 plt.show

### pyplot使用动态rc参数

pyplot 使用rc配置文件来定义图形的各种默认属性

plt.rcParams函数配置rc参数

线条常用的rc参数

lines.linewidth 线宽0-10
lines.linestyle 样式 '-'，'--' '-.' ':'
lines.marker    标记形状 'o','D','h' ，'.' ，','， 'S'
lines.marksize  标记大小0-10


绘图中文显示，默认不支持，需通过设置 font.sans-serif 、axes.unicode_minus 参数改变绘图时的字体
 
plt.rcParams['font.sans-serif'] = 'simhei'
plt.rcParams['axes.unicode_minus'] = False 正常显示符号

## 折线图

> 主要查看因变量y随自变量x改变的趋势，适合用于显示随时间而变化的连续数据
> 同时可以查看数量的差异、增长趋势的变化

* plt.plot 折线图

## 条形图

* plt.bar 竖直条形图
* plt.barh  水平条形图
  > left  接收array，x轴数据
    height 接收array, y轴代表数据的数量
    width   接收0-1之间的float 宽度
    color    string/颜色字符串的array， 条形图的颜色

## 直方图
> 质量分布图， 横轴代表类别，纵轴表示数量或占比

* hist( x, bins=None, range=None, density=False, weights=None,
          cumulative=False, bottom=None,
    > bins 表示bin的一个序列，默认10
    > normed 是否进行归一化处理
      color 直方图的颜色
      orientation  默认vertical 垂直。 horizontal 水平

## 饼图 Pie
> 反映

* plt.pie(x) 
    > x 饼图的数据
    > explode 指定离饼图圆心n个半径
    > labels 每一项的名称
    > color  饼图颜色
    > autopct 数值的显示方式
    > pctdistance  每一项的比例和距离饼图圆心n个半径
    > labeldistance 名称距离饼图圆心n个半径
    > radius 饼图半径 float 默认1
         
## 散点图 Scatter
> 利用坐标点的分布形态来反映特征间的统计关系的一种图形， 跨类别的数据比较
 
 * plt.scatter()
   > * x, y     表示xy轴的数据
   > * s        点的大小（数值/一维数组）
   > * c        点的颜色（数值/一维数组
   > * marker   点的标记类型（string）
   > * alpha    点的透明度（数值/一维数组

## 箱线图 boxplot
> 提供有关数据位置和分散情况的关键信息，尤其是在不同特征是，更可以表现其分散程度的差异

箱线图 的5个统计量 （最小值，下四分位数，中位数，上四分位数，最大值）

 * plt.boxplot()
   > * x            表示数据
   > * notch        中间箱体是否有缺口，默认None/False
   > * sym          异常点的形状
   > * vert         图形是横向或纵向 boolean
   > * positions    图形的位置
   > * widths       箱体的宽度
   > * labels       每个箱线图的标签
   > * meanline     是否显示均值线



