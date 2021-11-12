import numpy as np
from PIL import Image

from pillow_image import get_image


def make_tiff(dense=8, width=512, is_gray=True):
    if is_gray:
        arr = np.random.randint(1, pow(2, dense), (width, width), dtype=f'uint{dense}')
        if dense == 8:
            mode = 'L'
        else:
            mode = 'I;16'
    else:
        arr = np.random.randint(1, pow(2, dense), (width, width, 3), dtype=f'uint{dense}')
        if dense == 8:
            mode = 'RGB'  # 3x8位像素
        else:
            mode = 'RGB'  # 无法完成16位通道 https://pillow.readthedocs.io/en/stable/handbook/concepts.html#modes

    im = Image.fromarray(arr, mode=mode)
    im.save(f'f512x512_{dense}_{is_gray or "rgb"}.tiff')
    print(arr.shape, arr.dtype)
    print(arr[:10][:10])


if __name__ == '__main__':
    # name = r'C:\Users\dengxixi\Documents\WeChat Files\edgardeng\FileStorage\File\2021-11\gain.tif'
    # img = get_image(name)
    # data = np.array(img)
    # print(data.shape)
    # print(data[:10][:10])
    make_tiff(16, 512, False)
    make_tiff(8, 512, False)

    # img = get_image('../avatar.jpeg')
    # img = img.resize((512, 512))
    # # gray = img.convert("I")
    # # gray.save(r'd:\512x512_32.tiff')
    # gray = img.convert("L")
    # gray.save(r'd:\512x512_8.tiff')

    # img = np.uint16(np.array(gray))
    # print(img.shape)
    #
    # im = Image.fromarray(img, mode='I;16')
    # im.save(r'd:\512x512_16.tiff')

    # arr = np.random.randint(0, 512, (256,256), )
    # a = np.array(np.uint16(arr))
    # print(a[:10])
    # im = Image.fromarray(a)
    # im =Image.fromarray(a, mode='I;16')
    # im.save(r'd:\256x256.tiff')

    # img = get_image(r'd:\512x512_16.tiff')
    # img.show()
