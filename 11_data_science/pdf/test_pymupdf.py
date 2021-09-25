import datetime
import os

import fitz  # fitz就是pip install PyMuPDF -i https://mirrors.aliyun.com/pypi/simple (PyMuPDF-1.18.17)



def pdf_to_img(path_file):
    with fitz.open(path_file) as pdf:
        print(pdf.metadata)
        for i in range(pdf.pageCount):
            # if i < 118 or i > 120:
            #     continue
            path = path_file.replace('.pdf', f'{i}.jpg')
            page = pdf[i]
            pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5).preRotate(0))
            pix.writePNG(path)
            # pix.save(path)
            # mat = fitz.Matrix(1, 1).preRotate(0)
            # pix = page.getPixmap(matrix=mat, alpha=False)
            # pix.writePNG(path)


def img_to_pdf(list_path_img, path_pdf):
    doc = fitz.open()
    # 循环path中的文件，可import os 然后用 for img in os.listdir(img_path)实现
    # 这里为了让文件以1，2，3的形式进行拼接，就偷懒循环文件名中的数字。
    for img_file in list_path_img:
        imgdoc = fitz.open(img_file)
        pdfbytes = imgdoc.convertToPDF()  # 使用图片创建单页的 PDF
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)
    doc.save(path_pdf)
    doc.close()


if __name__ == "__main__":
    path = r'D:\聚均科技-研发\2021 聚均科技AI平台\OCR\上市公司财报.pdf'
    # path = r'D:\聚均科技-研发\2021 聚均科技AI平台\OCR\热力公司2016年审计报告.pdf'
    pdf_to_img(path)
    # list_img = ['热力公司2016年审计报告3.jpg', 'Inked热力公司2016年审计报告-4.jpg', '热力公司2016年审计报告6.jpg', '热力公司2016年审计报告9.jpg',
    #             '热力公司2016年审计报告4.jpg', ]
    # list_img = ['热力公司2016年审计报告3.jpg', 'Inked热力公司2016年审计报告6.jpg', '热力公司2016年审计报告9.jpg',]
    #
    # path2 = r'D:\聚均科技-研发\2021 聚均科技AI平台\OCR\热力公司2016年审计报告222.pdf'
    # list_img2 = [f'D:\聚均科技-研发\\2021 聚均科技AI平台\\OCR\\{item}' for item in list_img]
    # img_to_pdf(list_img2, path2)
