# -*- coding: utf-8 -*-
# @author: edgardeng
# @date:   2021-05-25
# @file:   使用PdfMine 提取文字 (pdfminer.six == 20201018)
import base64
import math
import time
import pdfminer
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfdocument import PDFTextExtractionNotAllowed, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

print('pdfminer.__version__:', pdfminer.__version__)

from pdfminer.layout import LAParams, LTTextContainer, LTChar
from PIL import Image, ImageDraw
import fitz
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from pathlib import Path

"""
从可读PDF中读取文字和坐标

待解决问题：
 1 text_box 和 text_line的关系
 2 无法提取: 电子印章 ，电子签名？？
 3 无法多线程读取一个pdf
"""

list_time = []


def extract_text_from_page(page_layout, scale=1, extract_character=False, ):
    '''
    从page中提取文字 ，(可使用多线程提取文字)
    :param page_layout: PDF页
    :param scale: 放大倍数
    :param extract_character 是否提取单个字符
    :return:
    '''
    t = time.time()
    page_bbox = page_layout.bbox
    page_w = page_bbox[2]
    page_h = page_bbox[3]
    page_result = {
        'w': page_w * scale,
        'h': page_h * scale
    }
    page_text = []
    page_character = []
    page_figure = []
    for element in page_layout:
        # Each element will be an LTTextBox, LTFigure, LTLine, LTRect or an LTImage.
        if isinstance(element, LTTextContainer):  # LTTextBoxHorizontal
            # print('element', text_line.get_text())
            for lt_text_line in element:  # LTTextLineHorizontal
                # x1 = round(lt_text_line.bbox[0] * scale)
                # y1 = round(page_h * scale - lt_text_line.bbox[1] * scale)
                # x2 = round(lt_text_line.bbox[2] * scale)
                # y2 = round(page_h * scale - lt_text_line.bbox[3] * scale)
                # text = lt_text_line.get_text().strip()
                # if len(text) == 0:
                #     continue
                # page_text.append((lt_text_line.get_text(), x1, y1, x2, y2))
                # if not extract_character:
                #     continue
                # print('text_line', lt_text_line.get_text())
                first_x1 = 0
                first_y1 = 0
                x2 = 0
                y2 = 0
                char_list = []
                for lt_char in lt_text_line:  # LTChar
                    if isinstance(lt_char, LTChar):
                        # print(character.fontname)
                        # print(character.size)
                        char = lt_char.get_text().strip()
                        if len(char) > 0:
                            x1 = math.floor(lt_char.bbox[0] * scale)
                            y1 = math.floor(page_h * scale - lt_char.bbox[1] * scale)
                            x2 = round(lt_char.bbox[2] * scale)
                            y2 = round(page_h * scale - lt_char.bbox[3] * scale)
                            if first_x1 == 0 and first_y1 == 0:
                                first_x1, first_y1 = x1, y1
                            char_list.append(char)
                            if extract_character:
                                page_character.append((char, x1, y1, x2, y2))
                if char_list:
                    page_text.append((''.join(char_list), first_x1, first_y1, x2, y2))
        else:
            print(type(element))
            if isinstance(element, pdfminer.layout.LTFigure):
                for im in element:
                    print(type(im))  # pdfminer.layout.LTImage
                    im_data = im.stream.get_rawdata()
                    x1 = round(im.bbox[0] * scale)
                    y1 = round(page_h * scale - im.bbox[1] * scale)
                    x2 = round(im.bbox[2] * scale)
                    y2 = round(page_h * scale - im.bbox[3] * scale)
                    img_b64 = str(base64.b64encode(im_data), encoding='utf-8')
                    page_figure.append((img_b64, x1, y1, x2, y2))

    page_result['text'] = page_text
    page_result['character'] = page_character
    page_result['figure'] = page_figure
    # print('use:', time.time() - t)
    list_time.append(time.time() - t)
    return page_result


def extract_text_from_pdf(path_file, scale=1.0, extract_character=False):
    """从可复制的pdf中 提取文字 """

    list_page_text = []
    i = 0
    t_start = time.time()
    path_pdf = Path(path_file)
    with path_pdf.open('rb') as fp:  # TODO 此处无法多线程读取一个文件
        parser = PDFParser(fp)
        doc = PDFDocument(parser, password='', caching=True)
        if not doc.is_extractable:
            return None
        laparams = LAParams()
        resource_manager = PDFResourceManager(caching=True)
        device = PDFPageAggregator(resource_manager, laparams=laparams)
        interpreter = PDFPageInterpreter(resource_manager, device)
        page_layouts = []
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            layout = device.get_result()
            page_layouts.append(layout)
    t2 = time.time()
    print('read pdf use:', t2 - t_start, '页数', len(page_layouts))
    print('*' * 20, ' extract_text_from_pdf 线程池')
    with ThreadPoolExecutor(max_workers=10) as pool:
        all_task = [pool.submit(extract_text_from_page, page, scale, extract_character) for page in page_layouts]
        wait(all_task, timeout=0, return_when=ALL_COMPLETED)

        for task in all_task:
            list_page_text.append(task.result())
        print('最大耗时', max(list_time))
        print('最小耗时', min(list_time))
        print('平均耗时', sum(list_time) / len(all_task))
    t_end = time.time()
    print('流程总共耗时', t_end - t_start)
    return list_page_text


def convert_pdf_image(path_file, dir_image, scale=1.0, text_bbox=None):
    '''
     将pdf转化为图片
    :param path_file:
    :param dir_image:
    :param text_box: 文字框位置 text,x1,y1,x2,y2
    :return:
    '''
    Path(dir_image).mkdir(exist_ok=True)
    path_pdf = Path(path_file)
    with fitz.open(path_file) as pdf:
        # print(pdf.metadata)
        for i in range(pdf.pageCount):
            page = pdf[i]  # fitz.fitz.Page
            # print(type(page), dir(page))
            pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale).preRotate(0))  # TODO 是否需要做旋转
            # print(type(pixmap), dir(pixmap))  # fitz.fitz.Pixmap
            cspace = pixmap.colorspace
            if cspace is None:
                mode = "L"
            elif cspace.n == 1:
                mode = "L" if pixmap.alpha == 0 else "LA"
            elif cspace.n == 3:
                mode = "RGB" if pixmap.alpha == 0 else "RGBA"
            else:
                mode = "CMYK"

            image = Image.frombytes(mode, (pixmap.width, pixmap.height), pixmap.samples)
            if not text_bbox:
                path_img = Path(dir_image).joinpath(f'{path_pdf.name}_{i}.png')
                image.save(str(path_img))
                continue

            draw = ImageDraw.Draw(image)
            page_bbox = text_bbox[i]
            if page_bbox.get('text'):
                for item_bbox in page_bbox.get('text'):
                    draw.rectangle([item_bbox[1], item_bbox[2], item_bbox[3], item_bbox[4]], fill=None, outline='green')
                path_img = Path(dir_image).joinpath(f'{path_pdf.name}_text{i}.png')
                image.save(str(path_img))
            if page_bbox.get('character'):
                if page_bbox.get('text'):
                    image = Image.frombytes(mode, (pixmap.width, pixmap.height), pixmap.samples)
                    draw = ImageDraw.Draw(image)
                for item_bbox in page_bbox.get('character'):
                    draw.rectangle([item_bbox[1], item_bbox[2], item_bbox[3], item_bbox[4]], fill=None,
                                   outline='orange')
                path_img = Path(dir_image).joinpath(f'{path_pdf.name}_character{i}.png')
                image.save(str(path_img))
            if page_bbox.get('figure'):
                for item_bbox in page_bbox.get('figure'):
                    draw.rectangle([item_bbox[1], item_bbox[2], item_bbox[3], item_bbox[4]], fill=None,
                                   outline='red')
                path_img = Path(dir_image).joinpath(f'{path_pdf.name}_figure{i}.png')
                image.save(str(path_img))


if __name__ == '__main__':
    scale_i = 1.5
    # pdf_path = r'D:\聚均科技-研发\2021 聚均科技AI平台\OCR\中登网\46.pdf'
    # pdf_path = r'text_position.pdf'
    # pdf_path = r'zhichan_127.pdf'
    pdf_path = r'han_zhang-12.pdf'
    # pdf_path = r'fapiao.pdf'
    t = time.time()
    print('start', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    result = extract_text_from_pdf(pdf_path, scale_i, True)
    print('end use:%.2f' % (time.time() - t))
    if result is None or not result[0].get('text'):
        print('extract none text')
    convert_pdf_image(pdf_path, 'jpg', scale_i, result)
