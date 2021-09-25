# -*- coding: utf-8 -*-
# @author: edgardeng
# @date:   2021-05-25
# @file:   使用PdfMine 提取文字 pdfminer.six == 20201018
import time

import pdfminer
from pdfminer.high_level import extract_text, extract_pages
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextContainer, LTChar
# from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from PIL import Image
import fitz
import re
import os

from pathlib import Path

COLOR_BLUE = (255, 0, 0)
print('pdfminer.__version__:', pdfminer.__version__)


def read_pdf_text(path_file, extract_character = False):
    """从可复制的pdf中 提取文字 """

    list_text = []
    page_wh = None
    from pdfminer.high_level import extract_pages
    i = 0
    for page_layout in extract_pages(path_file):
        print('*' * 10, i)

        i += 1
        if i < 11:
            continue
        page_text = []
        for element in page_layout:
            # Each element will be an LTTextBox, LTFigure, LTLine, LTRect or an LTImage.
            if isinstance(element, LTTextContainer):
                if not extract_character:
                    page_text.append((element.get_text(), *element.bbox))
                    continue
                for text_line in element:
                    for character in text_line:
                        if isinstance(character, LTChar):
                            print(character.fontname)
                            print(character.size)
                            page_text.append((character.get_text(), *character.bbox))
            else:
                print(type(element))
                print((element.get_text(), *element.bbox))
        # rotate = int(0)
        # trans = fitz.Matrix(1, 1).preRotate(rotate)
        # pm = page_layout.getPixmap(matrix=trans, alpha=False)
        # path = 'a.png'
        # pm.writePNG(path)

        list_text.append(page_text)
        page_wh = page_layout.bbox
    print(list_text[0])
    print(page_wh)
    return list_text
    # print(list_text[0])




def write_pdf_image(path_file, text_bbox):
    import cv2
    path_pdf = Path(path_file)
    with fitz.open(path_file) as pdf:
        # print(pdf.metadata)
        for i in range(pdf.pageCount):
            if i >= 9:
                break
            # if i < 118 or i > 120:
            #     continue
            bbox = text_bbox[i]
            tmp = str(path_pdf.parent.joinpath('temp.png'))  # path_file.replace('.pdf', f'tmp.jpg')
            # path = path_file.replace('.pdf', f'{i}.jpg')
            page = pdf[i]
            pix = page.get_pixmap(matrix=fitz.Matrix(1, 1).preRotate(0))
            pix.writePNG(tmp)
            time.sleep(0.1)
            print(tmp)
            cv_img = cv2.imread(tmp)
            for item in bbox:
                cv2.rectangle(cv_img, (int(item[1]), 842 - int(item[2])), (int(item[3]), 842 - int(item[4])),
                              COLOR_BLUE, 1)
            path_png = path_pdf.parent.joinpath('jpg').joinpath(f'{i}.png')
            cv2.imwrite(str(path_png), cv_img)
            # while True:
            #     cv2.imshow("image", cv_img)
            #     if cv2.waitKey(0) & 0xFF == 27:
            #         break


def write_pdf_pic(path_pdf, text_bbox):
    from pdf2image import convert_from_path
    import numpy as np
    import cv2
    images = convert_from_path(path_pdf)
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    for index, image_pil in enumerate(images):

        # 得到这一页图片
        # image_pil = image[i]
        # 把这一页的图片格式转成numpy类型
        image_numpy = cv2.resize(np.array(image_pil), (595, 842), interpolation=cv2.INTER_AREA)
        bbox = text_bbox[index]
        for item in bbox:
            cv2.rectangle(image_numpy, (int(item[1]), 842 - int(item[2])), (int(item[3]), 842 - int(item[4])),
                          COLOR_BLUE, 2)
            cv2.putText(image_numpy, '*' * len(item[0].strip()), (int(item[1]) + 2, 842 - int(item[2]) + 2), font, 1.2,
                        COLOR_BLUE, 2)
            # image_numpy = np.array(image_pil)

        # 得到这一页图片德国高度，为了之后得到实际的box
        while True:
            cv2.imshow("image", image_numpy)
            if cv2.waitKey(0) & 0xFF == 27:
                break


class GetPic:
    def __init__(self, filename, password=''):
        """
        初始化
        :param filename: pdf路径
        :param password: 密码
        """
        file = open(filename, 'rb')
        self.parser = PDFParser(file)
        # 创建文档
        self.doc = PDFDocument(self.parser, password)
        # 连接文档与文档分析器
        # self.parser.set_document(self.doc)
        # self.doc.set_parser(self.parser)
        # 初始化, 提供初始密码, 若无则为空字符串
        # self.doc.initialize(password)
        # 检测文档是否提供txt转换, 不提供就忽略, 抛出异常
        if not self.doc.is_extractable:
            print('doc.is_extractable')
            # raise PDFTextExtractionNotAllowed
        else:
            # 创建PDF资源管理器, 管理共享资源
            self.resource_manager = PDFResourceManager()
            # 创建一个PDF设备对象
            self.laparams = LAParams()
            self.device = PDFPageAggregator(self.resource_manager, laparams=self.laparams)
            # 创建一个PDF解释器对象
            self.interpreter = PDFPageInterpreter(self.resource_manager, self.device)
            # pdf的page对象列表
            self.doc_pdfs = list(self.doc.get_pages())
        #  打开PDF文件, 生成一个包含图片doc对象的可迭代对象
        # self.doc_pics = fitz.open(filename)

    def to_pic(self, doc, zoom, pg, pic_path):
        """
        将单页pdf转换为pic
        :param doc: 图片的doc对象
        :param zoom: 图片缩放比例, type int, 数值越大分辨率越高
        :param pg: 对象在doc_pics中的索引
        :param pic_path: 图片保存路径
        :return: 图片的路径
        """
        rotate = int(0)
        trans = fitz.Matrix(zoom, zoom).preRotate(rotate)
        pm = doc.getPixmap(matrix=trans, alpha=False)
        path = os.path.join(pic_path, str(pg)) + '.png'
        pm.writePNG(path)
        return path

    def get_pic_loc(self, doc):
        """
        获取单页中图片的位置
        :param doc: pdf的doc对象
        :return: 返回一个list, 元素为图片名称和上下y坐标元组组成的tuple. 当前页的尺寸
        """
        self.interpreter.process_page(doc)
        layout = self.device.get_result()
        # pdf的尺寸, tuple, (width, height)
        canvas_size = layout.bbox
        # 图片名称坐标
        loc_top = []
        # 来源坐标
        loc_bottom = []
        # 图片名称与应截取的区域y1, y2坐标
        loc_named_pic = []
        # 遍历单页的所有LT对象
        for i in layout:
            if hasattr(i, 'get_text'):
                text = i.get_text().strip()
                # 匹配关键词
                if re.search(r'图表*\s\d+[:：]', text):
                    loc_top.append((i.bbox, text))
                elif re.search(r'来源[:：]', text):
                    loc_bottom.append((i.bbox, text))
        zip_loc = zip(loc_top, loc_bottom)
        for i in zip_loc:
            y1 = i[1][0][1]
            y2 = i[0][0][3]
            name = i[0][1]
            loc_named_pic.append((name, (y1, y2)))
        return loc_named_pic, canvas_size

    def get_crops(self, pic_path, canvas_size, position, cropped_pic_name, cropped_pic_path):
        """
        按给定位置截取图片
        :param pic_path: 被截取的图片的路径
        :param canvas_size: 图片为pdf时的尺寸, tuple, (0, 0, width, height)
        :param position: 要截取的位置, tuple, (y1, y2)
        :param cropped_pic_name: 截取的图片名称
        :param cropped_pic_path: 截取的图片保存路径
        :return:
        """
        img = Image.open(pic_path)
        # 当前图片的尺寸 tuple(width, height)
        pic_size = img.size
        # 截图的范围扩大值
        size_increase = 10
        x1 = 0
        x2 = pic_size[0]
        y1 = pic_size[1] * (1 - (position[1] + size_increase) / canvas_size[3])
        y2 = pic_size[1] * (1 - (position[0] - size_increase) / canvas_size[3])
        cropped_img = img.crop((x1, y1, x2, y2))
        # 保存截图文件的路径
        path = os.path.join(cropped_pic_path, cropped_pic_name) + '.png'
        cropped_img.save(path)
        print('成功截取图片:', cropped_pic_name)

    def main(self, pic_path, cropped_pic_path, pgn=None):
        """
        主函数
        :param pic_path: 被截取的图片路径
        :param cropped_pic_path: 图片的截图的保存路径
        :param pgn: 指定获取截图的对象的索引
        :return:
        """
        if pgn is not None:
            # 获取当前页的doc
            doc_pdf = self.doc_pdfs[pgn]
            doc_pic = self.doc_pics[pgn]
            # 将当前页转换为PNG, 返回值为图片路径
            path = self.to_pic(doc_pic, 2, pgn, pic_path)
            loc_name_pic, canvas_size = self.get_pic_loc(doc_pdf)
            if loc_name_pic:
                for i in loc_name_pic:
                    position = i[1]
                    cropped_pic_name = re.sub('/', '_', i[0])
                    self.get_crops(path, canvas_size, position, cropped_pic_name, cropped_pic_path)


def read_pdf2(path_file):
    from io import StringIO

    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfparser import PDFParser

    output_string = StringIO()
    with open(path_file, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        # outlines = doc.get_outlines()
        # for (level,title,dest,a,se) in outlines:
        #     print (level, title)

        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    print(output_string.getvalue())


def read_pdf_page(path_file):
    from pdfminer.layout import LTTextContainer, LTChar
    pages = extract_pages(path_file)
    for page_layout in pages:
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                print(element.get_text())
                print('-' * 40)
                for text_line in element:
                    for character in text_line:
                        if isinstance(character, LTChar):
                            print(character.fontname)
                            print(character.size)
                            print('*' * 40)


if __name__ == '__main__':
    # path = r'D:\聚均科技-研发\2021 聚均科技AI平台\OCR\天津锦湖三年报表\2020年12月财务报表.pdf'
    # path = r'D:\聚均科技-研发\2021 聚均科技AI平台\OCR\天津锦湖三年报表\2019年审计报告.pdf'

    # read_pdf_text(path)
    # read_pdf(path)
    # read_pdf2(path)
    # read_pdf_page(path)

    pdf_path = r'text_position.pdf'
    # pdf_path = r'zhichan_127.pdf'
    pdf_path = r'han_zhang-12.pdf'
    result = read_pdf_text(pdf_path, True)
    write_pdf_image(pdf_path, 'jpg')
    # write_pdf_pic(pdf_path, result)
    # test = GetPic(pdf_path)
    # pic_path = 'PNG的保存路径'
    # cropped_pic_path = '截图的保存路径'
    # page_count = test.doc_pics.pageCount
    # for i in range(page_count):
    #     test.main(pic_path, cropped_pic_path, pgn=i)
