import os
import PyPDF2

pdf_dir = '/Users/kk/Downloads/135.李笑来谈AI时代的家庭教育【完结】' # pdf文件目录
merged_pdf = PyPDF2.PdfFileWriter()

# 获取所有pdf文件的路径,并按文件名排序
files = os.listdir(pdf_dir)
# NB 改变当前路径
os.chdir(pdf_dir)

# 对文件名排序 
files.sort()

# pdf_paths = sorted(os.listdir(pdf_dir), key=lambda x: int(os.path.splitext(x)[0])) 

# 遍历每个pdf文件,添加到PdfFileWriter中
for path in files:
    if(not path.endswith('.pdf')):
        continue
    pdf_path = os.path.join(pdf_dir, path)
    pdf = PyPDF2.PdfFileReader(open(pdf_path, 'rb'))

    bk_name = path
    bk_flag = False
    for page in range(pdf.getNumPages()):
        merged_pdf.addPage(pdf.getPage(page))
        if not bk_flag:
            merged_pdf.addBookmark(bk_name, len(merged_pdf.pages) - 1) 
            bk_flag = True
    
    
# 写入合并后的pdf文件
with open('merged.pdf', 'wb') as f:
    merged_pdf.write(f)