# -*- coding: utf-8 -*-
# @author: edgardeng (https://github.com/edgardeng)
# @date:   2021-02-08
# @file:   使用pillow自定义画图
from PIL import ImageDraw, Image


def draw_image():
    """ 自定义画一张图 """
    size = (200, 200)
    img = Image.new('RGB', size, (255, 255, 255))
    # 划线
    draw = ImageDraw.Draw(img)
    draw.line((0, 0) + img.size, fill=120)
    draw.line((0, img.size[1], img.size[0], 0), fill=120)
    img.save('line.png')
    # text（xy, text, fill, font, spacing, direction:有rtl，ttb两种）:
    draw.text((10, 10), 'text', fill='red')
    img.save('text.png')
    # 画圆 arc（xy，start，end，fill）：
    draw.arc([20, 20, 60, 60], 0, 270, fill='red')  # box, start angle, end angle, fill color
    img.save('circle.png')
    # chord（xy, start, end, fill, outline）: 和arc功能相同，outline是划线颜色，而fill是填充颜色。与arc的区别是，画完图之后，会将末位点和起始点连接起来
    draw.chord([60, 60, 120, 100], 0, 270, fill='blue', outline='yellow')
    img.save('chrod.png')
    # pieslice（）： 参数和功能都和chord一样，区别在于最后将末位点与起始点连接到中心：
    draw.pieslice([10, 100, 80, 160], 0, 270, fill='blue', outline='yellow')
    img.save('pieslice.png')
    # ellipse（） 画椭圆
    draw.ellipse([100, 20, 160, 60], fill='red')  # box, start angle, end angle, fill color
    img.save('ellipse.png')

    # rectangle（xy，fill,outline） 画举行
    draw.rectangle([160, 160, 180, 190], fill='red', outline='green')
    img.save('rectangle.png')
    # polygon(xy, fill, outline) 多边形
    draw.polygon([90, 60, 110, 60, 130, 80, 80, 150], fill='gray',outline='orange' )
    img.save('polygon.png')
    # point(xy, fill) 画点点
    draw.point([60, 60, 62, 60, 64, 60, 66, 60, 68, 60, 70, 60], fill='black')
    img.save('points.png')

    img.close()


if __name__ == '__main__':
    draw_image()
