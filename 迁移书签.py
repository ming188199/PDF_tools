#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import re
from pdf2image import convert_from_path 
from PIL import Image

import pathlib
import PyPDF2


# dir_input = input('请输入文件路径：')
# curr_dir = pathlib.Path(dir_input)
curr_dir = pathlib.Path('/Users/kk/Downloads/张遇升《给忙碌者的大脑健康课》/给忙碌者的大脑健康课(pdf)/')
path_img = curr_dir/'img/'
os.chdir(path_img)

filename_targe = input('请输入目标PDF名称：')
# 读取源PDF文件并获取书签信息
pdf = PyPDF2.PdfFileReader('result.pdf')
bookmarks = pdf.getOutlines()

# 读取目标PDF文件,准备添加书签
pdf_writer = PyPDF2.PdfFileWriter()
pdf_writer.cloneReaderDocumentRoot(PyPDF2.PdfFileReader(filename_targe))

# 遍历书签,获取位置和名称
for bookmark in bookmarks:
    page_num = bookmark.page
    title = bookmark.title
    # 添加书签
    bookmark_page = pdf_writer.addBookmark(title, page_num)

# 输出新的PDF
with open(filename_targe, 'wb') as f:
    pdf_writer.write(f)


