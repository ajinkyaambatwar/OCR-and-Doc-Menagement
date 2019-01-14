import pytesseract
import time
from word_search import file_process
import cv2
from file_max import file_handler
import subprocess as sp
from PIL import Image
import pandas as pd
import numpy as np
from check import is_grey_scale

def apply_ocr(img_path):
    command = ['tesseract', img_path, 'eng', 'txt', 'tsv']
    sp.run(command)


#text=pytesseract.image_to_string(Image.open('emirates_id_8.jpg'),'ara+eng')


def get_emirates_data(filename):
    try:
        cif_no = filename.split('_')[-1].split('.')[0]
    except:
        cif_no = str(np.random.randint(1000000,2000000))
    
    img=cv2.imread(filename)
    apply_ocr(filename)
    text=pytesseract.image_to_string(Image.open(filename),'ara+eng')
    with open('textfile.txt','w') as file:
        file.writelines(text)
    time.sleep(0.5)
    content=file_process('textfile.txt')
    print(content)
    for line in content:
        if "Name" in line:
            name_index=content.index(line)
        if "Nationality" in line:
            nat_index=content.index(line)

    arabic_name_index=name_index-1
    arabic_name=content[arabic_name_index]
    index_arabic_name=arabic_name.find(':')
    name_in_arabic=arabic_name[index_arabic_name+1:]

    arabic_nationality_index=nat_index-1
    arabic_nationality=content[arabic_nationality_index]
    index_arabic_nationality=arabic_nationality.find(':')
    nationality_in_arabic=arabic_nationality[index_arabic_nationality+1:]
    '''
    df = pd.read_csv('eng.tsv', sep='\t')
    df=df[df.text != ' ']

    df = df.dropna()
    footer = df[df.block_num == df.block_num.max()]
    footer_coords = [(footer.iloc[0].left-20, footer.iloc[0].top-20), (footer.iloc[-1].left+footer.iloc[-1].width+20, footer.iloc[-1].top+footer.iloc[-1].height+20)]
    print(footer_coords)
    img2=img[footer_coords[0][1]:footer_coords[1][1],footer_coords[0][0]:footer_coords[1][0]]

    # cv2.imshow('cut',img2)
    # cv2.waitKey()
    cv2.imwrite("results.png",img2)
    time.sleep(1)
    a=Image.open("results.png")

    text=pytesseract.image_to_string(a)

    text=text.replace(" ",'')
    text2=text.replace('\n','')
    '''
    text2=file_handler(filename)
    print(text2)
    Data= {'type': 'emirates_id','name':None,'card_no':None,'emirates_id':None,'birth_date':None,'expiry_date':None,'nationality':None,'sex':None, 'cif_no': cif_no,'arabic_name':None,'nationality(arabic)':None}
    Data['card_no']=text2[5:14]
    Data['emirates_id']=text2[15:30]
    year_store=text2[30:32]
    birth_month=text2[32:34]
    birth_date=text2[34:36]
    if int(year_store) > 30:
        year='19'+year_store
    else:
        year='20'+year_store

    birth_day=birth_date+'/'+birth_month+'/'+year
    Data["birth_date"]=birth_day
    Data['sex']=text2[37]
    expiry_year='20'+text2[38:40]
    expiry_month=text2[40:42]
    expiry_date=text2[42:44]
    Data["expiry_date"]=expiry_date+'/'+expiry_month+'/'+expiry_year
    Data["nationality"]=text2[45:48]
    last_line=text2[60:]
    index=last_line.find('<')
    last_name=last_line[0:index]
    next_string=last_line[index+2:]
    index2=next_string.find('<')
    first_name=next_string[0:index2]
    last_string=last_line[index+2+index2+1:]
    index3=last_string.find('<')
    middle_name=last_string[0:index3]
    name=first_name+' '+middle_name+' '+last_name
    Data['name']=name
    # print(Data)
    return Data

data=get_emirates_data('Jordanian Emirates ID.png')
print(data)

