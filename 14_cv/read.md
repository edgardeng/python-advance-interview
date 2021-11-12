# Python 机器视觉

## OpenCV

### 图像读取和写入

#### 读取图片，返回图片对象 cv2.imread()

 * img_path: 图片的路径，即使路径错误也不会报错，但打印返回的图片对象为None
 * flag：cv2.IMREAD_COLOR，读取彩色图片，图片透明性会被忽略，为默认参数，也可以传入1
     cv2.IMREAD_GRAYSCALE,按灰度模式读取图像，也可以传入0
     cv2.IMREAD_UNCHANGED,读取图像，包括其alpha通道，也可以传入-1
####  cv2.imshow(window_name,img)：显示图片，窗口自适应图片大小
    * window_name: 指定窗口的名字
    * img：显示的图片对象
可以指定多个窗口名称，显示多个图片

#### cv2.waitKey(millseconds)  键盘绑定事件，阻塞监听键盘按键，返回一个数字（不同按键对应的数字不同）
millseconds: 传入时间毫秒数，在该时间内等待键盘事件；传入0时，会一直等待键盘事件

#### cv2.destroyAllWindows(window_name)
window_name: 需要关闭的窗口名字，不传入时关闭所有窗口
#### cv2.imwrite((img_path_name,img)
 * img_path_name:保存的文件名
 * img：文件对象

#### 添加边界 cv2.copyMakeBorder()
参数：
* img:图像对象
* top,bottom,left,right: 上下左右边界宽度，单位为像素值
* borderType:
    * cv2.BORDER_CONSTANT, 带颜色的边界，需要传入另外一个颜色值
    * cv2.BORDER_REFLECT, 边缘元素的镜像反射做为边界
    * cv2.BORDER_REFLECT_101/cv2.BORDER_DEFAULT
    * cv2.BORDER_REPLICATE, 边缘元素的复制做为边界
    * CV2.BORDER_WRAP
* value: borderType为cv2.BORDER_CONSTANT时，传入的边界颜色值，如[0,255,0]

### 像素运算
#### 像素相加 cv2.add()
参数：
img1:图片对象1
img2:图片对象2
mask:None （掩膜，一般用灰度图做掩膜，img1和img2相加后，和掩膜与运算，从而达到掩盖部分区域的目的）
dtype:-1

注意：图像相加时应该用cv2.add(img1,img2)代替img1+img2    
```python
x = np.uint8([250])
y = np.uint8([10])
cv2.add(x,y) # 250+10 = 260 => 255  #相加，opencv超过255的截取为255
x+y          # 250+10 = 260 % 256 = 4  #相加，np超过255的会取模运算 （uint8只能表示0-255，所以取模）

```

#### 加权相加 cv2.addWeighted() 两张图片相加，分别给予不同权重，实现图片融合和透明背景等效果
参数： (img1*alpha+img2*beta+gamma)
 * img1: 图片对象1
* alpha: img1的权重
* img2: 图片对象2
* beta:img1的权重
* gamma：常量值，图像相加后再加上常量值
* dtype：返回图像的数据类型，默认为-1，和img1一样
 

### 位运算

#### cv2.btwise_and(): 与运算
  参数：
  img1:图片对象1
  img2:图片对象2
  mask:掩膜
#### cv2.bitwise_or()：或运算
  参数：
  img1:图片对象1
  img2:图片对象2
  mask:掩膜
####cv2.bitwise_not(): 非运算
  img1:图片对象1
  mask:掩膜
####cv2.bitwise_xor():异或运算，相同为1，不同为0（1^1=0,1^0=1）
  img1:图片对象1
  img2:图片对象2
  mask:掩膜

### 2.7 图像颜色空间转换

#### cv2.cvtColor()
参数：
 * img: 图像对象
* code：
    * cv2.COLOR_RGB2GRAY: RGB转换到灰度模式
    cv2.COLOR_RGB2HSV： RGB转换到HSV模式（hue,saturation,Value）
#### cv2.inRange()
参数：
 * img: 图像对象/array
 * lowerb: 低边界array，  如lower_blue = np.array([110,50,50])
 * upperb：高边界array， 如 upper_blue = np.array([130,255,255])

 `mask = cv2.inRange(hsv, lower_green, upper_green)`

### 2.8 性能评价

#### cv2.getTickCount()： 获得时钟次数

#### cv2.getTickFrequency()：获得时钟频率 （每秒振动次数

### 3. 图像阈值化
####   cv2.threshold():
   参数：
   * img:图像对象，必须是灰度图
   * thresh:阈值
   * maxval：最大值
   * type:
       * cv2.THRESH_BINARY:      小于阈值的像素置为0，大于阈值的置为maxval
       * cv2.THRESH_BINARY_INV： 小于阈值的像素置为maxval，大于阈值的置为0
       * cv2.THRESH_TRUNC：      小于阈值的像素不变，大于阈值的置为thresh
       * cv2.THRESH_TOZERO       小于阈值的像素置0，大于阈值的不变
       * cv2.THRESH_TOZERO_INV   小于阈值的不变，大于阈值的像素置0
     
   返回两个值
    * ret:阈值
    * img：阈值化处理后的图像

#### cv2.adaptiveThreshold() 自适应阈值处理，图像不同部位采用不同的阈值进行处理
参数：
 * img: 图像对象，8-bit单通道图
 * maxValue:最大值
 * adaptiveMethod: 自适应方法
    * cv2.ADAPTIVE_THRESH_MEAN_C     ：阈值为周围像素的平均值
    * cv2.ADAPTIVE_THRESH_GAUSSIAN_C : 阈值为周围像素的高斯均值（按权重）
 * threshType:
    * cv2.THRESH_BINARY:     小于阈值的像素置为0，大于阈值的置为maxValuel
    * cv2.THRESH_BINARY_INV:  小于阈值的像素置为maxValue，大于阈值的置为0
 * blocksize: 计算阈值时，自适应的窗口大小,必须为奇数 （如3：表示附近3个像素范围内的像素点，进行计算阈值） * C： 常数值，通过自适应方法计算的值，减去该常数值
(mean value of the blocksize*blocksize neighborhood of (x, y) minus C)

### 4. 图像形状变换
#### 4.1 * * cv2.resize()   图像缩放

    参数：
*  src: 输入图像对象
* dsize：输出矩阵/图像的大小，为0时计算方式如下：dsize = Size(round(fx*src.cols),round(fy*src.rows))
* fx: 水平轴的缩放因子，为0时计算方式：  (double)dsize.width/src.cols
* fy: 垂直轴的缩放因子，为0时计算方式：  (double)dsize.heigh/src.rows
* interpolation：插值算法
   * cv2.INTER_NEAREST : 最近邻插值法
   * cv2.INTER_LINEAR   默认值，双线性插值法 (适合于图像放大)
   * cv2.INTER_AREA      (适合于图像缩小)  基于局部像素的重采样（resampling using pixel area relation）。对于图像抽取（image decimation）来说，这可能是一个更好的方法。但如果是放大图像时，它和最近邻法的效果类似。
   * cv2.INTER_CUBIC        基于4x4像素邻域的3次插值法 (适合于图像放大)
   * cv2.INTER_LANCZOS4     基于8x8像素邻域的Lanczos插值 

#### 4.2 cv2.warpAffine()     仿射变换

仿射变换（从二维坐标到二维坐标之间的线性变换，且保持二维图形的“平直性”和“平行性”。仿射变换可以通过一系列的原子变换的复合来实现，包括平移，缩放，翻转，旋转和剪切）

参数：
 * img: 图像对象
 * M：2*3 transformation matrix (转变矩阵)
 * dsize：输出矩阵的大小,注意格式为（cols，rows）  即width对应cols，height对应rows
 * flags：可选，插值算法标识符，有默认值INTER_LINEAR，
    如果插值算法为WARP_INVERSE_MAP, warpAffine函数使用如下矩阵进行图像转dst(x,y)=src(M11*x+M12*y+M13,M21*x+M22*y+M23)
    borderMode：可选， 边界像素模式，有默认值BORDER_CONSTANT
    borderValue:可选，边界取值，有默认值Scalar()即0

#### 4.2.1 平移变换 cv2.warpAffine(img,M,(cols,rows))
> ，平移变换只是采用了一个如下的转变矩阵（transformation matrix）: 从（x,y）平移到（x+tx, y+ty）

#### 4.2.3 旋转变换 cv2.getRotationMatrix2D()  返回2*3的转变矩阵（浮点型）
    参数：
        center：旋转的中心点坐标
        angle：旋转角度，单位为度数，证书表示逆时针旋转
        scale：同方向的放大倍数

#### 4.2.4 仿射变换矩阵的计算

通过上述的平移，缩放，旋转的组合变换即实现了仿射变换，上述多个变换的变换矩阵相乘即能得到组合变换的变换矩阵。同时该变换矩阵中涉及到六个未知数（2*3的矩阵），通过变换前后对应三组坐标，也可以求出变换矩阵，opencv提供了函数getAffineTransform()来计算变化矩阵

cv2.getAffineTransform()  返回2*3的转变矩阵
参数：
src：原图像中的三组坐标，如np.float32([[50,50],[200,50],[50,200]])
dst: 转换后的对应三组坐标，如np.float32([[10,100],[200,50],[100,250]])

### 4.3 透视变换(persperctive transformation)

仿射变换都是在二维空间的变换，透视变换（投影变换）是在三维空间中发生了旋转。需要前后四组坐标来计算对应的转变矩阵，opencv提供了函数getPerspectiveTransform()来计算转变矩阵，cv2.warpPerspective()函数来进行透视变换。其对应参数如下：

#### cv2.getPerspectiveTransform()   返回3*3的转变矩阵
参数：    
src：原图像中的四组坐标，如 np.float32([[56,65],[368,52],[28,387],[389,390]])
dst: 转换后的对应四组坐标，如np.float32([[0,0],[300,0],[0,300],[300,300]])


        cv2.warpPerspective()
        参数：    
            src: 图像对象
            M：3*3 transformation matrix (转变矩阵)
            dsize：输出矩阵的大小，注意格式为（cols，rows）  即width对应cols，height对应rows
            flags：可选，插值算法标识符，有默认值INTER_LINEAR，
                   如果插值算法为WARP_INVERSE_MAP, warpAffine函数使用如下矩阵进行图像转dst(x,y)=src(M11*x+M12*y+M13,M21*x+M22*y+M23)
            borderMode：可选， 边界像素模式，有默认值BORDER_CONSTANT 
            borderValue:可选，边界取值，有默认值Scalar()即0

#### 对坐标点进行透视变换，对于原图像上的一点，通过perspctiveTransform()能计算出透视变换后图片上该点的坐标，其对应参数如下：

cv2.perspectiveTransform(src, matrix)

参数：
 * src：坐标点矩阵，注意其格式. 如src=np.array([[589, 91],[1355, 91],[1355, 219],[589, 219]], np.float32).reshape(-1, 1, 2), 表示四个坐标点，size为(4, -1, 2)
 * matrix：getPerspectiveTransform()得到的透视变换矩阵 返回值：变换后的坐标点，格式和src相同


## [Pillow](./pillow/readme.md)
 
### 颜色的命名

* RGB方法，命名形式是这样的：rgb（red，green，blue）。
三颜色参数，分别表示色道值，在0-255之间。
也可用0-100%来进行赋值。这和我们html里面设置长宽有些类似，我们除了width：500px之外，还可以用width：50%来表示。

* HSL方法，Hue-Saturation-Lightness。
色调，饱和度，明度。表示形式：hsl（h, s, l）。
Hue（色调）的取值在0-360之间，0代表red，120代表green，240代表blue。
Saturation（饱和度）取值0-100%，0代表灰（gray），100代表全颜色（full color）。
Lightness（明度）取值也在0-100%，0代表black，50位normal（正常），100位white。

* HSV方法，和HSL同，除了V（value），取值0-100%，0为black，100位normal。
还有一种，HSB，B（brightness）亮度，参数要求和HSV相同。

