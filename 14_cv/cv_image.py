# -*- coding: utf-8 -*-
# @author: edgardeng (https://github.com/edgardeng)
# @date:   2021-02-08
# @file:   使用cv2操作图片
import cv2
import numpy as np
from matplotlib import pyplot as plt


def get_image(path_img):
    """ 读入一张图片 """
    img = cv2.imread(path_img)  # 打开图片
    print(f'Type: {type(img)}')
    print(f'Image Shape: {img.shape}')
    print(f'Image Size(w*h*dim): {img.size}')
    print(f'Image dtype(w*h*dim): {img.dtype}')
    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # ret, img_threshold = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
    # cv2.imshow("img", img)
    # cv2.imshow("threshold", img_threshold)
    #
    # key = cv2.waitKey(0)
    # if key == 27:  # 按esc键时，关闭所有窗口
    #     print(key)
    #     cv2.destroyAllWindows()
    # cv2.imwrite(r"cv_threshold.jpg", img_threshold)


def handle_pixel():
    print('-' * 10, '2.3 图像像素获取和编辑')
    img = cv2.imread('avatar.jpeg')
    # 获取和设置
    pixel = img[100, 100]  # [57 63 68],获取(100,100)处的像素值
    img[100, 100] = [57, 63, 99]  # 设置像素值
    b = img[100, 100, 0]  # 57, 获取(100,100)处，blue通道像素值
    g = img[100, 100, 1]  # 63
    r = img[100, 100, 2]  # 68
    r = img[100, 100, 2] = 99  # 设置red通道值
    # 获取和设置
    piexl = img.item(100, 100, 2)
    img.itemset((100, 100, 2), 99)

    # ROI,Range of instrest
    roi = img[100:200, 300:400]  # 截取100行到200行，列为300到400列的整块区域
    img[50:150, 200:300] = roi  # 将截取的roi移动到该区域 （50到100行，200到300列）

    b = img[:, :, 0]  # 截取整个蓝色通道
    b, g, r = cv2.split(img)  # 截取三个通道，比较耗时
    img2 = cv2.merge((b, g, r))
    cv2.imshow('roi', img)
    cv2.waitKey(0)


def border():
    img2 = cv2.imread('avatar.jpeg')
    img = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)  # matplotlib的图像为RGB格式
    constant = cv2.copyMakeBorder(img, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=[0, 255, 0])  # 绿色
    reflect = cv2.copyMakeBorder(img, 20, 20, 20, 20, cv2.BORDER_REFLECT)
    reflect01 = cv2.copyMakeBorder(img, 20, 20, 20, 20, cv2.BORDER_REFLECT_101)
    replicate = cv2.copyMakeBorder(img, 20, 20, 20, 20, cv2.BORDER_REPLICATE)
    wrap = cv2.copyMakeBorder(img, 20, 20, 20, 20, cv2.BORDER_WRAP)
    titles = ["constant", "reflect", "reflect01", "replicate", "wrap"]
    images = [constant, reflect, reflect01, replicate, wrap]
    for i in range(5):
        plt.subplot(2, 3, i + 1), plt.imshow(images[i]), plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    plt.show()


def pixel_cal():
    # 2.5 像素算术运算
    import numpy as np
    img1 = cv2.imread('avatar.jpeg', 0)
    roi_img = np.zeros(img1.shape[0:2], dtype=np.uint8)
    # print(img1.shape[0:2])
    roi_img[100:280, 400:550] = 255

    img_add = cv2.add(img1, img1)
    img_add_mask = cv2.add(img1, img1, mask=roi_img)
    cv2.imshow("img_add", img_add)
    cv2.imshow("img_add_mask", img_add_mask)

    img_2 = cv2.imread('scenery.jpeg')
    img_1 = cv2.resize(cv2.imread('avatar.jpeg'), (img_2.shape[0], img_2.shape[1]))
    blend = cv2.addWeighted(img_1, 0.5, img_2, 0.9, 0)  # 两张图的大小和通道也应该相同
    cv2.imshow("blend", blend)
    cv2.waitKey(0)


def pixel_bit_call():
    img1 = cv2.resize(cv2.imread('avatar.jpeg'), (400, 400))
    rows, cols = img1.shape[0:2]
    img2 = cv2.imread('scenery.jpeg')
    roi = img2[0:rows, 0:cols]
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    ret, img1_thres = cv2.threshold(img1_gray, 200, 255, cv2.THRESH_BINARY_INV)
    img1_fg = cv2.add(img1, img1, mask=img1_thres)  # 拿到logo图案的前景

    img1_thres_inv = cv2.bitwise_not(img1_thres)
    roi_bg = cv2.add(roi, roi, mask=img1_thres_inv)  # 拿到roi图案的背景

    img_add = cv2.add(img1_fg, roi_bg)  # 背景和前景相加
    img2[0:rows, 0:cols] = img_add

    cv2.imshow("gray", img1_gray)
    cv2.imshow("thres", img1_thres)
    cv2.imshow("fg", img1_fg)
    cv2.imshow("tinv", img1_thres_inv)
    cv2.imshow("roi_bg", roi_bg)
    cv2.imshow("img_add", img_add)
    cv2.imshow("img2", img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def track_bar():
    def nothing(args):
        pass

    img = cv2.imread(r"scenery.jpeg")
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.namedWindow('tracks')
    cv2.createTrackbar("LH", "tracks", 0, 255, nothing)
    cv2.createTrackbar("LS", "tracks", 0, 255, nothing)
    cv2.createTrackbar("LV", "tracks", 0, 255, nothing)

    cv2.createTrackbar("UH", "tracks", 255, 255, nothing)
    cv2.createTrackbar("US", "tracks", 255, 255, nothing)
    cv2.createTrackbar("UV", "tracks", 255, 255, nothing)

    # switch = "0:OFF \n1:ON"
    # cv2.createTrackbar(switch,"tracks",0,1,nothing)

    while True:
        l_h = cv2.getTrackbarPos("LH", "tracks")
        l_s = cv2.getTrackbarPos("LS", "tracks")
        l_v = cv2.getTrackbarPos("LV", "tracks")
        u_h = cv2.getTrackbarPos("UH", "tracks")
        u_s = cv2.getTrackbarPos("US", "tracks")
        u_v = cv2.getTrackbarPos("UV", "tracks")

        lower_b = np.array([l_h, l_s, l_v])
        upper_b = np.array([u_h, u_s, u_v])

        mask = cv2.inRange(img_hsv, lower_b, upper_b)
        res = cv2.add(img, img, mask=mask)

        cv2.imshow("img", img)
        cv2.imshow("mask", mask)
        cv2.imshow("res", res)
        k = cv2.waitKey(1)
        if k == 27:
            break
    cv2.destroyAllWindows()


def handle_threshold():
    img = cv2.imread(r"scenery.jpeg", 0)

    ret, thre1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    adaptive_thre1 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 7, 2)
    adaptive_thre2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 2)

    titles = ["img", "thre1", "adaptive_thre1", "adaptive_thre2"]
    imgs = [img, thre1, adaptive_thre1, adaptive_thre2]

    for i in range(4):
        plt.subplot(2, 2, i + 1), plt.imshow(imgs[i], "gray")
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
    plt.show()


def otsus_binarization():
    img = cv2.imread('scenery.jpeg', 0)

    # global thresholding
    ret1, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # Otsu's thresholding
    ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(img, (5, 5), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # plot all the images and their histograms
    images = [img, 0, th1,
              img, 0, th2,
              blur, 0, th3]
    titles = ['Original Noisy Image', 'Histogram', 'Global Thresholding (v=127)',
              'Original Noisy Image', 'Histogram', "Otsu's Thresholding",
              'Gaussian filtered Image', 'Histogram', "Otsu's Thresholding"]

    for i in range(3):
        plt.subplot(3, 3, i * 3 + 1), plt.imshow(images[i * 3], 'gray')
        plt.title(titles[i * 3]), plt.xticks([]), plt.yticks([])
        plt.subplot(3, 3, i * 3 + 2), plt.hist(images[i * 3].ravel(), 256)
        plt.title(titles[i * 3 + 1]), plt.xticks([]), plt.yticks([])
        plt.subplot(3, 3, i * 3 + 3), plt.imshow(images[i * 3 + 2], 'gray')
        plt.title(titles[i * 3 + 2]), plt.xticks([]), plt.yticks([])
    plt.show()


def transformation():
    print('向左平移100，向下平移50')
    img = cv2.imread('scenery.jpeg', 0)
    rows, cols = img.shape
    M = np.float32([[1, 0, 100], [0, 1, 50]])
    dst = cv2.warpAffine(img, M, (cols, rows))
    cv2.imwrite('scenery-transfrom.jpg', dst)

    print('# 4.2.4 仿射变换矩阵的计算')
    img = cv2.imread('scenery.jpeg')
    rows, cols, ch = img.shape

    pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
    pts2 = np.float32([[10, 100], [200, 50], [100, 250]])

    M = cv2.getAffineTransform(pts1, pts2)  # 根据变换前后三组坐标计算变换矩阵　　　 返回2*3的转变矩阵
    dst = cv2.warpAffine(img, M, (cols, rows))

    plt.subplot(121), plt.imshow(img), plt.title('Input')
    plt.subplot(122), plt.imshow(dst), plt.title('Output')
    plt.show()
    print('4.3 透视变换(persperctive transformation)')

    pts1 = np.float32([[56, 65], [368, 52], [28, 387], [389, 390]])
    pts2 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])

    M = cv2.getPerspectiveTransform(pts1, pts2)

    dst = cv2.warpPerspective(img, M, (300, 300))

    plt.subplot(121), plt.imshow(img), plt.title('Input')
    plt.subplot(122), plt.imshow(dst), plt.title('Output')
    plt.show()

    matrix = np.float32([[ 8.06350904e-01, -1.67497791e-02, -4.34096149e+01],
                         [ 2.85178118e-02,  8.29440456e-01, -6.26063898e+01],
                        [ 2.41877972e-05,  1.99790270e-05 , 1.00000000e+00]])

    rect = np.array([[589, 91], [1355, 91], [1355, 219], [589, 219]], np.float32)
    rect = rect.reshape(-1, 1, 2)
    newRect = cv2.perspectiveTransform(rect, matrix) # 对坐标点进行透视变换，对于原图像上的一点，通过perspctiveTransform()能计算出透视变换后图片上该点的坐标
    print(newRect)

    rect_fill = np.ones((4, 3), dtype=np.float32)
    rect_fill[:, :2] = rect
    mid_rect = np.dot(matrix, rect_fill.T)
    mid_rect = mid_rect.T
    mid_rect[:, :2] = mid_rect[:, :2]/mid_rect[:, 2:]
    print("TEST", mid_rect)


if __name__ == '__main__':
    # get_image('avatar.jpeg')
    # handle_pixel()
    # border()
    # pixel_cal()
    # pixel_bit_call()
    # track_bar()
    # handle_threshold()
    # otsus_binarization()
    transformation()
