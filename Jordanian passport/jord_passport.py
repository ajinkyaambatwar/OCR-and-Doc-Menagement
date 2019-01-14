
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


def jord_passport(filename):

    text2=file_handler(filename)
    text2=list(text2)
    #print(len(text2))
    if len(text2) > 88:
        del text2[40:40+len(text2)-88]
    if len(text2)<88:
        text2.insert(41,"<")
    print(len(text2))
    text2="".join(text2)
    print(text2)
    Data= {'Name':None,'Passport Number':None,'National Number':None,'Date Of Birth':None,'Expiry Date':None,'Nationality':None,'Sex':None}

    #---Name----
    name_string=str(text2[5:])
    index=name_string.find('<')
    name1=name_string[0:index]
    forward_string=name_string[index+2:]
    index2=forward_string.find('<')
    name2=forward_string[0:index2]
    final_string=forward_string[index2+1:]
    index3=final_string.find('<')
    name3=final_string[0:index3]
    Data["Name"]=name1+" "+name2+" "+name3

    #----Passport Number
    Data["Passport Number"]=text2[44:51]

    #---Nationality
    Data["Nationality"]=text2[54:57]

#----Birth Dateext2[57:59]
    year_store=text2[57:59]
    print(year_store)
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

    Data["National Number"]=text2[72:81]
    return Data

data=jord_passport('s3-passport.jpg')
print(data)