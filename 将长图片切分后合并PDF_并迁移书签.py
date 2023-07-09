

import os
from pdf2image import convert_from_path
from PIL import Image

from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import pathlib

def pdf_to_img(pdf_path):
    pages = convert_from_path(pdf_path)
    image_counter = 1
    for page in pages:
        if image_counter == 1:
            file_save_name = f'{os.path.splitext(pdf_path)[0]}.jpg'
        else:
            file_save_name = f'{os.path.splitext(pdf_path)[0]}_{image_counter}.jpg'
            print(file_save_name)
        page.save(file_save_name, 'JPEG')
        image_counter = image_counter + 1
def img_split(path):
    img = Image.open(path)
    width, height = img.size
    
    # 计算切割后的片段数量
    split_width = width
    split_num_w = 1
    split_height = width * 1.4
    split_num_h = int(height // split_height)
    
    # 获取图片主色调
    main_color = get_main_color(img)
    
    # 开始切割
    i = 0
    sum_offset = 0 #总偏移 初始化
    offset = 5
    for j in range(split_num_h+1):
        # 计算切割区域 sum_offset 上次总偏移
        x1, x2 = 0, split_width
        y1, y2 = j*split_height + sum_offset + int(j>0)*offset, min((j+1)*split_height, img.height)
        area = (x1, y1, x2, y2)

        # 检查切割线附近的颜色,判断是否过于接近文本
        # if is_nearlywhite(img, area, main_color, 5):  
        #     continue   # 跳过切割
        sum_offset = 0 #总偏移清零
        while not is_nearlywhite(img, area, main_color, offset):
            sum_offset += offset
            y2 = min((j+1)*split_height + sum_offset, img.height)
            area = (x1, y1, x2, y2)
            if y2 == img.height:
                break
        if y1 >= y2:
            continue
        crop_img = img.crop(area)  
        # 保存切割后的片段
        # print(f'{path_img}/{os.path.splitext(curr_dir)[0]}.jpg')
        filename_bigjpg = pathlib.Path(filename).stem
        last_str = str(filename_bigjpg)[-1]
        if last_str.isdigit():
            filename_jpg = filename_bigjpg[0:-1]
        else:
            last_str = '0'
            filename_jpg = filename_bigjpg
        crop_img.save(f'{path_img}/{filename_jpg}_{last_str}_{j:02d}.jpg')
    print(path_img/f'{filename_jpg}_{last_str}_{j:02d}.jpg')


# 获取图片主色调            
def get_main_color(img):
    # 将图片转换为RGB模式
    img = img.convert('RGB')
    
    # 获取图片尺寸
    width, height = img.size
    
    # 统计图片中RGB值出现的次数
    rgb_dict = {}
    for i in range(width):
        for j in range(min(height, 1000)):
            rgb = img.getpixel((i,j))
            if rgb not in rgb_dict:
                rgb_dict[rgb] = 1
            else:
                rgb_dict[rgb] += 1
                
    # 将字典按value值排序,取出现次数最多的颜色        
    rgb_sorted = sorted(rgb_dict.items(), key=lambda x:x[1], reverse=True)
    
    # 返回RGB值最高的颜色            
    return rgb_sorted[0][0]  

def get_linearea_4point(img, area, offset):
    x1, y1, x2, y2 = area
    # 扩大offset个像素
    x1_o = x1 - offset
    y1_o = y2 - offset
    x2_o = x2 + offset
    y2_o = y2 + offset

    # 校验扩大后的区域是否超出图像范围
    x1_o = max(x1_o, 0)
    y1_o = int(min(max(y1_o, 0), img.height))
    x2_o = int(min(x2_o, img.width))
    y2_o = int(min(y2_o, img.height))
    return (x1_o, y1_o, x2_o, y2_o)


# 检查指定区域附近是否为白色或背景色        
def is_nearlywhite(img, area, main_color, offset):
    # 获取切割区域左上角和右下角位置
    x1, y1, x2, y2 = area
    (x1_o, y1_o, x2_o, y2_o) = get_linearea_4point(img, area, offset)
    if y1_o >= y2_o:
        return True
    # 统计扩大区域内每个像素的值
    rgb_dict = {}
    rgb_dict[main_color] = 0
    for i in range(x1_o, x2_o):
        for j in range(y1_o, y2_o):
            rgb = img.getpixel((i,j))
            if rgb not in rgb_dict:
                rgb_dict[rgb] = 1
            else:
                rgb_dict[rgb] += 1  
                
    # 如果主色调的像素值大于80% 或 最近的其他颜色值不超过10%
    if rgb_dict[main_color] > 0.95 * (x2_o - x1_o) * (y2_o - y1_o) \
            or rgb_dict[max(rgb_dict, key=rgb_dict.get)] < 0.05 * (x2_o - x1_o) * (y2_o - y1_o):
        return True
    else:
        return False

import PyPDF2
def bookmarks_new_pdf():
    filename_targe = input('等abbyy OCR生成新的PDF后，请输入目标PDF名称：')
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

from PIL import Image
import img2pdf
from PyPDF2 import PdfFileMerger
from io import BytesIO


dir_input = input('请输入文件夹目录')
curr_dir = pathlib.Path(dir_input)
path_img = curr_dir/'img/'

# 1. pdf2img
if not path_img.exists():
    # 递归遍历所有pdf文件
    for filename in curr_dir.rglob('*.pdf'):
        # print(pathlib.Path(filename).stem)
        pdf_to_img(filename)
# 建立图片文件夹
path_img.mkdir()

# 递归遍历所有jpg文件并切割
for filename in curr_dir.glob('*.jpg'):
    print(filename)
    # img = Image.open(filename)
    img_split(filename)

files = os.listdir(path_img)
# NB 改变当前路径
os.chdir(path_img)

# curr_dir = pathlib.Path('.')
# # 获取所有文件
# files = os.listdir(curr_dir)

# 对文件名排序 
files.sort()
# 使用lambda表达式获取文件名中的数字部分
# files.sort(key=lambda f: int(f.split('_')[2])) 


# 初始化PdfFileMerger对象
merger = PdfFileMerger()

# 遍历图片并添加到PDF
# for img in files:
#     if not img.endswith('.jpg'):
#         continue
for img in sorted(path_img.glob('*.jpg'), key = lambda img : (img.stem)):
    # 打开图片
    # print(img)
    image = Image.open(img)  

    img_str = img.stem
    # 图片转换为PDF页面
    page = img2pdf.convert(img_str+'.jpg')

    # 添加页面
    f = BytesIO(page) 
    merger.append(f)

    # 为指定图片添加书签
    if img_str.endswith('_0_00'):
        bk_name = (img_str[0:len(img_str)-len('_0_00')])
        bkmk = merger.addBookmark(bk_name, len(merger.pages) - 1) 
        print(bk_name)


# 输出PDF文件 
merger.write('result.pdf')

# 迁移书签
bookmarks_new_pdf()

