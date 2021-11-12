## Pillow

> PIL：Python Imaging Library，已经是Python平台事实上的图像处理标准库.
> [Github](https://github.com/python-pillow/Pillow),
> [Handbook](https://pillow.readthedocs.io/en/latest/handbook/index.html)
  
### 图像读取

* open 读取一个图像文件
  > im = Image.open("1.png")
  > im.format, im.size, im.mode
* ImageGrab.grab 截屏
  > im = ImageGrab.grab ((0,0,800,200)) #截取屏幕指定区域的图像 #不带参数表示全屏幕截图

* convert(mode) 图像色彩转换

    * 1 (1-bit pixels, black and white, stored with one pixel per byte)
    * L (8-bit pixels, black and white)
    * P (8-bit pixels, mapped to any other mode using a colour palette)
    * RGB (3x8-bit pixels, true colour)
    * RGBA (4x8-bit pixels, true colour with transparency mask)
    * CMYK (4x8-bit pixels, colour separation)
    * YCbCr (3x8-bit pixels, colour video format)
    * I (32-bit signed integer pixels)
    * F (32-bit floating point pixels)
    
* histogram 图像直方图

### 图像操作

#### Resize

* 图像裁剪 im.crop
* 图像粘贴 im.paste(region, box)
* 缩放 im.resize((100,100))
*

#### Filter

* 高斯模糊 `im.filter(ImageFilter.GaussianBlur)`
* 普通模糊 im.filter(ImageFilter.BLUR)
* 边缘增强 im.filter(ImageFilter.EDGE_ENHANCE)
* 找到边缘 im.filter(ImageFilter.FIND_EDGES)
* 浮雕 im.filter(ImageFilter.EMBOSS)
* 轮廓 im.filter(ImageFilter.CONTOUR)
* 锐化 im.filter(ImageFilter.SHARPEN)
* 平滑 im.filter(ImageFilter.SMOOTH)
* 细节 im.filter(ImageFilter.DETAIL)

#### ImageEnhance 图像增强

* 亮度增强 `ImageEnhance.Brightness(image).enhance(1.5)`
* 色度增强 `ImageEnhance.Color(image).enhance(1.5)`
* 对比度增强 `ImageEnhance.Contrast(image).enhance(1.5)`
* 锐度增强 `ImageEnhance.Sharpness(image).enhance(1.5)`

#### transpose 图像变换

* im.rotate(45) # 逆时针旋转 45 度角。
* im.transpose(Image.FLIP_LEFT_RIGHT)       #左右对换。
* im.transpose(Image.FLIP_TOP_BOTTOM)       #上下对换。
* im.transpose(Image.ROTATE_90)             #旋转 90 度角。
* im.transpose(Image.ROTATE_180)            #旋转 180 度角。
* im.transpose(Image.ROTATE_270)            #旋转 270 度角。

### Image 类

Image 类是 PIL 库中一个非常重要的类，通过这个类来创建实例可以有直接载入图像文件，读取处理过的图像和通过抓取的方法得到的图像这