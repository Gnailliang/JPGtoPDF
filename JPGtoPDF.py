import os
import sys
from fpdf import FPDF
from PIL import Image,ExifTags
import re

def CheckJPG(path):
    flag = True
    datanames = os.listdir(path)
    fname = "\n"
    for dataname in datanames:
        if os.path.splitext(dataname)[-1] != '.jpg'or'.JPG'or'JPEG'or "PNG" or "png":
            fname = fname + dataname + '\n'
    if flag == False:
        print("\n\n如下文件非JPG格式，请核对后再转换："+fname+"\n\n")
    return flag  


def JPGtoPDF(path):
    print(os.path.basename(path))

    imagelist = [i for i in os.listdir(path)]

    pdf = FPDF(orientation="P",unit="mm",format="A4")
    pdf.set_auto_page_break(0)
    
    if not os.path.isdir(os.path.join(path,'temp')):
        os.makedirs(os.path.join(path,'temp'),mode=0o777)

    for im in sorted(imagelist,key=lambda x:int(re.findall('\d+',x)[0])):
        imgPath = os.path.join(path,im)
        img = Image.open(imgPath)
        if imgPath.endswith(".png") or imgPath.endswith(".PNG"):
            img = img.convert('RGB')

        if hasattr(img, "_getexif") and isinstance(img._getexif(), dict):
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation]=='Orientation':break   
            exif=dict(img._getexif().items())
            if exif[orientation] == 3 : 
                 img=img.rotate(180, expand = True)
            elif exif[orientation] == 6 : 
                img=img.rotate(270, expand = True)
            elif exif[orientation] == 8 : 
                img=img.rotate(90, expand = True)  
        img.save(os.path.join(path,'temp',im))
        print(im) 

        pdf.add_page() 
        pdf.image(os.path.join(os.path.join(path,"temp",im)),w=190,h=0)
    print("等待合成PDF文档......\n") 
    pdf.output(os.path.join(path, os.path.basename(path)+".pdf"), "F")
    print("JPG转PDF成功，请在路径“"+path+"”下查阅\n") 


print('\n--------------------------------------------------------------')
print("将jpg/jpeg格式图片转换成PDF文件\n")
print("图片放到一个文件夹里，名字需要含数字.会按数字顺序生成PDF.\n")
print("Ver0.00.03 ")
print("2023-02-09 首版 for 欣宇")
print("2023-07-03 更新 for 盼盼")


while True:  
    try:

        path = input("-----------请输入图片文件夹路径,并按回车键开始转换------------\n")
        if CheckJPG(path):
             JPGtoPDF(path)  
    except Exception as e: 
        print("JPG转PDF发生错误，错误代码:", e)
    os.system("pause")