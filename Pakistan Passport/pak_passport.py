import cv2
import numpy as np
import time
import pytesseract
import pandas as pd
import subprocess as sp
import csv
from file_max import file_handler


def apply_ocr(img_path):
    command = ['tesseract', img_path, 'eng', 'txt', 'tsv']
    sp.run(command)

def return_data(filename):
    '''img=cv2.imread(filename)
    apply_ocr(filename)
    df = pd.read_csv('eng.tsv',sep='\t',quoting=csv.QUOTE_NONE)
    df=df[df.text != ' ']
    df.dropna()
    footer = df[df.block_num == df.block_num.max()]
    footer_coords = [(footer.iloc[0].left-20, footer.iloc[0].top-20), (footer.iloc[-1].left+footer.iloc[-1].width+20, footer.iloc[-1].top+footer.iloc[-1].height+20)]
    print(footer_coords)
    img2=img[footer_coords[0][1]:footer_coords[1][1],footer_coords[0][0]:footer_coords[1][0]]
    cv2.imshow('cut',img2)
    cv2.waitKey(0)

    #------Running tesseract on ---------
    text=pytesseract.image_to_string(img2)
    text=text.replace(" ",'')
    text2=text.replace('\n','')
    print(text2)
    '''
    text2=file_handler(filename)
    text2=list(text2)
    #print(len(text2))
    if len(text2) > 88:
        del text2[40:40+len(text2)-88]
    if len(text2)<88:
        text2.insert(41,"<")
    Data= {'Name':None,'Passport Number':None,'ID Number':None,'Date Of Birth':None,'Expiry Date':None,'Nationality':None,'Sex':None}

    #---Name----
    name_string=text2[5:]
    index=name_string.find('<')
    name1=name_string[0:index]
    forward_string=name_string[index+2:]
    index2=forward_string.find('<')
    name2=forward_string[0:index2]
    final_string=forward_string[index2+1:]
    index3=final_string.find('<')
    name3=final_string[0:index3]
    Data["Name"]=name1+" "+name2+" "+name3

    #---Passport Numer
    Data["Passport Number"]=text2[44:54]

    #---Nationality____
    Data['Nationality']=text2[54:57]

    #----Birth Date
    year_store=text2[57:59]
    birth_month=text2[59:61]
    birth_date=text2[61:63]
    if int(year_store) > 30:
        year='19'+year_store
    else:
        year='20'+year_store

    birth_day=birth_date+'/'+birth_month+'/'+year
    Data["Date Of Birth"]=birth_day 

    #--Sex---
    Data['Sex']=text2[64]


    #---Expiry Date-----
    expiry_year='20'+text2[65:67]
    expiry_month=text2[67:69]
    expiry_date=text2[69:71]
    Data["Expiry Date"]=expiry_date+'/'+expiry_month+'/'+expiry_year

    #---ID number---
    Data["ID Number"]=text2[72:84]
    return Data
