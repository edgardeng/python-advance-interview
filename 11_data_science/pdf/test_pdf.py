# -*- coding: utf-8 -*-
# @author: edgardeng
# @date:   2021-05-25
# @file:   demo fo PyPDF4

import PyPDF4


def read_pdf(path_file):
    with open(path_file, 'rb') as file:
        reader = PyPDF4.PdfFileReader(file)

        information = reader.getDocumentInfo()
        number_of_pages = reader.numPages
        txt = f"""
        Information about {path_file}:
        Author: {information.author}
        Creator: {information.creator}
        Producer: {information.producer}
        Subject: {information.subject}
        Title: {information.title}
        Number of pages: {number_of_pages}
        """
        print(txt)


        for i in range(reader.numPages):
            print('*' * 40)
            page = reader.getPage(i)
            print(page.extractText())
            print('-'*40)
            print(page.getContents())



if __name__ == '__main__':
    path = r'D:\聚均科技-研发\2021 聚均科技AI平台\OCR\天津锦湖三年报表\2020年12月财务报表.pdf'
    read_pdf(path)
