# -*- coding: utf-8 -*-
# @author: edgardeng
# @date:   2021-05-25
# @file:   demo fo PyPDF4

import pdfplumber


def read_pdf(path_file):
    with pdfplumber.open(path_file) as pdf:
        print(pdf.metadata)
        for page in pdf.pages:
            # print('*' * 40)
            # print(page.extract_text())
            print('---------- 表格数据 ----------')
            for table in page.extract_tables():
                for row in table:
                    print(row)


def pdf_to_img(path_file):
    with pdfplumber.open(path_file) as pdf:
        print(pdf.metadata)
        i = 1
        for page in pdf.pages:
            i += 1
            if i < 98 or i > 108:
                continue
            im = page.to_image()
            path = path_file.replace('.pdf', f'{i}.jpg')
            im.save(path, format="JPEG")



if __name__ == '__main__':
    path = r'D:\聚均科技-研发\2021 聚均科技AI平台\OCR\天津锦湖三年报表\2020年12月财务报表.pdf'
    # path = r'D:\聚均科技-研发\2021 聚均科技AI平台\OCR\天津锦湖三年报表\2019年审计报告.pdf'
    path = r'D:\聚均科技-研发\2021 聚均科技AI平台\OCR\热力公司2016年审计报告.pdf'
    path = r'D:\聚均科技-研发\2021 聚均科技AI平台\OCR\上市公司财报.pdf'
    # read_pdf'(path)
    pdf_to_img(path)
