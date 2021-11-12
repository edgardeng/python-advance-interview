# -*- coding: utf-8 -*-
# @author: edgardeng (https://github.com/edgardeng)
# @date:   2021-02-08

from PIL import Image, ImageFilter, ImageEnhance, ImageColor


def get_image(img_path):
    # 打开图片，获取一些属性
    img = Image.open(img_path)  # 打开图片
    w, h = img.size  # 获得图像尺寸
    print(f'Image Type: {type(img)}')
    print(f'Original Size: {w},{h}')
    print(f'Format: {img.format}')
    print(f'Color Mode: {img.mode}')
    print(f'调色板 Palette: {img.palette}')
    print(f'Info: {img.info}')
    return img


def handle_image(img):
    w, h = img.size
    img.save('copy.jpg', 'JPEG')

    # 剪切
    box = (100, 100, 200, 200)  # 左 上 右 下
    croped_img = img.crop(box)
    croped_img.save('croped.jpg')
    # 粘贴
    box2 = (w - 200, h - 200, w - 100, h - 100)  # 左 上 右 下
    img.paste(croped_img, box2)
    img.save('paste.jpg', 'jpeg')

    # 修改图片的大小
    resize_img = img.resize((2000, 1250))
    resize_img.save('resize.jpg')
    # 旋转
    out = img.rotate(45)  #
    out.save('rotate.jpg')
    # transpose
    # out = img.transpose(Image.FLIP_LEFT_RIGHT)
    out = img.transpose(Image.FLIP_TOP_BOTTOM)
    out.save('transpose.jpg')
    # convert
    convert_img = img.convert('L')
    convert_img.save("convert_L.jpg")
    # merge 合并颜色通道
    r, g, b = img.split()
    bgr_img = Image.merge('RGB', (b, g, r))
    bgr_img.save('merge.jpg')
    # 缩放
    img.thumbnail((160, 160))
    img.save('thumbnail.jpg', 'jpeg')
    # img.show()  # 使用本机程序显示图片


def handle_image_filter(img):
    """ 过滤器的使用 """
    out = img.filter(ImageFilter.DETAIL)  # 细节处理
    out.save('filter.jpg')

    source = img.split()
    r, g, b = 0, 1, 2
    mask = source[r].point(lambda i: i < 100 and 255)  # where red is less than 100
    # process the green band
    out = source[g].point(lambda i: i * 0.7)
    # paste the processed band back, but only where red was < 100
    source[g].paste(out, None, mask)
    # build a new multiband image
    im = Image.merge(img.mode, source)
    im.save('popa.jpg')

    r, g, b = img.split()
    r = r.point(lambda i: i * 0.1)
    im = Image.merge(im.mode, (r, g, b))
    im.save('no_red.jpg')

    # .Enhance 增强
    enh = ImageEnhance.Contrast(img)
    enh.enhance(1.3).save('contrast.jpg')


def handle_png():
    # 混合 img1 加载 img2上
    img1 = Image.open('b.jpeg')
    img1.resize((960, 960))
    img2 = Image.open('avatar.jpeg')
    Image.blend(img1, img2, 0.5).save('blend.pngg')

    Image.alpha_composite(img1, img2)  # 把im2复合到im1上，


def handle_image_color():
    """ 颜色 的使用 """
    # 直拼
    print(ImageColor.getrgb('red'))
    print(ImageColor.getrgb('orange'))
    #
    print(ImageColor.getcolor('red', 'RGB'))
    print(ImageColor.getcolor('orange', 'RGBA'))  # convert a color string to an RGB tuple

    print(ImageColor.getrgb('rgb(255, 0, 0)'))
    print(ImageColor.getrgb('rgb(100%, 0%, 0%)'))
    print(ImageColor.getrgb(
        'hsl(0, 100%, 50%)'))  # hue 0-360 0r 120g 240b saturation 0-100% 0灰色 100全彩 lightness 0黑 50正常 100白 高速逻辑函数什么鬼  色调 饱和度 亮点
    print(ImageColor.getrgb('hsv(0, 100%, 100%)'))  # hue saturation value 0-100% 0黑 100正常
    print(ImageColor.getrgb('hsb(0, 100%, 100%)'))  # brightness


if __name__ == '__main__':
    img = get_image('avatar.jpeg')
    handle_image(img)
    # handle_image_filter(img)
    # handle_png()
    # handle_image_color()
