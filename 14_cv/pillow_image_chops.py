# -*- coding: utf-8 -*-
# @author: edgardeng (https://github.com/edgardeng)
# @date:   2021-02-08
# @file:   图片像素点运算 Channel Operations

from PIL import ImageChops, Image


def handle_image_pixel():
    img1 = Image.open('avatar.jpeg')
    img2 = Image.open('scenery.jpeg')
    # 叠加 add(image1, image2, scale=1.0, offset=0)[source] :: out = ((image1 + image2) / scale + offset)
    ops_img = ImageChops.add(img1, img2, scale=2, offset=100)
    ops_img.save('chops_add.jpg')
    # .add_modulo(image1, image2)[source] #:: out = ((image1 + image2) % MAX)
    ops_img = ImageChops.add_modulo(img1, img2)
    ops_img.save('chops_add_modulo.jpg')
    #  blend(image1, image2, alpha)[source] Alias for PIL.Image.Image.blend().
    ops_img = ImageChops.blend(img1, img2.resize(img1.size), 0.5)
    ops_img.save('chops_blend.jpg')

    # composite(image1, image2, mask)[source] : Alias for PIL.Image.Image.composite().
    # A mask image.  This image can have mode "1", "L", or "RGBA", and must have the same size as the other two images
    ops_img = ImageChops.composite(img1, img2, Image.new('L', img1.size))
    ops_img.save('chops_composite.jpg')

    # .constant(image, value)[source]  # Fill a channel with a given grey level.
    ops_img = ImageChops.constant(img1, 200)
    ops_img.save('chops_constant.jpg')
    # darker(image1, image2)[source] :: # out = min(image1, image2)
    ops_img = ImageChops.darker(img1, img2)
    ops_img.save('chops_darker.jpg')
    # difference(image1, image2)[source] # out = abs(image1 - image2)
    ops_img = ImageChops.difference(img1, img2)
    ops_img.save('chops_difference.jpg')

    # duplicate(image)[source] Alias for PIL.Image.Image.copy().
    # PIL.ImageChops.invert(image)[source] # out = MAX - image
    # PIL.ImageChops.lighter(image1, image2)[source] out = max(image1, image2)
    # PIL.ImageChops.logical_and(image1, image2)[source] # Logical AND between two images. # out = ((image1 and image2) % MAX)
    # PIL.ImageChops.logical_or(image1, image2)[source] # Logical OR between two images. # out = ((image1 or image2) % MAX)
    # PIL.ImageChops.multiply(image1, image2)[source] # Superimposes two images on top of each other. # out = image1 * image2 / MAX
    # If you multiply an image with a solid black image, the result is black. If you multiply with a solid white image, the image is unaffected.

    # PIL.ImageChops.offset(image, xoffset, yoffset=None)[source]
    # Returns a copy of the image where data has been offset by the given distances.
    # Data wraps around the edges. If yoffset is omitted, it is assumed to be equal to xoffset.
    # 参数:
    # xoffset – The horizontal distance.
    # yoffset – The vertical distance. If omitted, both distances are set to the same value.


    # PIL.ImageChops.screen(image1, image2)[source] #:: out = MAX - ((MAX - image1) * (MAX - image2) / MAX)
    # Superimposes two inverted images on top of each other.
    ops_img = ImageChops.screen(img1, img2)
    ops_img.save('chops_screen.jpg')
    # PIL.ImageChops.subtract(image1, image2, scale=1.0, offset=0)[source] #:: out = ((image1 - image2) / scale + offset)
    # Subtracts two images, dividing the result by scale and adding the offset. If omitted, scale defaults to 1.0, and offset to 0.0.
    ops_img = ImageChops.subtract(img1, img2)
    ops_img.save('chops_subtract.jpg')

    # PIL.ImageChops.subtract_modulo(image1, image2)[source] # out:: = ((image1 - image2) % MAX)
    # Subtract two images, without clipping the result.
    ops_img = ImageChops.subtract_modulo(img1, img2)
    ops_img.save('chops_subtract_modulo.jpg')


if __name__ == '__main__':
    handle_image_pixel()
