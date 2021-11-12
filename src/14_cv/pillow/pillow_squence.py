# -*- coding: utf-8 -*-
# @author: edgardeng (https://github.com/edgardeng)
# @date:   2021-02-08
# @file:   使用pillow 生产图片，GIF处理
import imageio  # 第三发库
from PIL import Image, ImageDraw, ImageSequence


def make_gif():
    """ 制作一张GIF图片 """

    def make_number_img(t):
        size = (80, 60)
        img = Image.new('RGB', size, (255, 255, 255))
        # 创建Font对象:
        # font = ImageFont.truetype('Arial.ttf', 36)
        # 创建Draw对象:
        draw = ImageDraw.Draw(img)
        draw.text((35, 25), t, fill='red')
        img.save('n.jpg', 'jpeg')
        return img

    frames = [make_number_img(t) for t in list('123456789')]  # imageio.imread(i)
    gif_path = 'numbers.gif'
    imageio.mimsave(gif_path, frames, 'GIF', duration=0.2)
    return gif_path


def get_dif_image(img_path):
    img = Image.open(img_path)
    # img.seek(1) #skip to the second frame
    try:
        while True:
            img.save(str(img.tell() + 1) + '.gif')
            img.seek(img.tell() + 1)  # 当到达最后一张图片的时候，再seek下一个就会出错了
    except EOFError:  # the sequence ends
        pass

    for frame in ImageSequence.Iterator(img):
        print(type(frame))


if __name__ == '__main__':
    gif_path = make_gif()
    get_dif_image(gif_path)
