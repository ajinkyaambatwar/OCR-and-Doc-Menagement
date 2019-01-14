import pytesseract
import time
from word_search import file_process
import cv2
import time
import subprocess as sp
from PIL import Image
import pandas as pd
import numpy as np
import os
from check import is_grey_scale
from is_arabic import only_arabic_chars
'''
def apply_ocr(img_path):
    command = ['tesseract', img_path, 'eng', 'txt', 'tsv']
    sp.run(command)
'''
arabic_character={}
def is_arabic(uchr):
    try: return arabic_character[uchr]
    except KeyError:
         return arabic_character.setdefault(uchr, 'ARABIC' in ud.name(uchr))

def only_roman_chars(unistr):
    return all(is_arabic(uchr)
           for uchr in unistr
           if uchr.isalpha()) # isalpha suggested by John Machin

def textcleaner(img_path):
    #command= ['bash', 'textcleaner', '-g -e stretch -f 25 -o 10 -s 1',img_path, 'cleaned.jpg']
    #print(command)
    #sp.run(command)
    os.system('bash textcleaner -g -e stretch -f 25 -o 10 -s 1 ' +img_path+' cleaned.jpg')
def extract_arabic(filename):
        img=Image.open(filename)
        text=pytesseract.image_to_string(img,'ara+eng')
        img.close()
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

        if only_arabic_chars(content[name_index-1]):
            arabic_name_index=name_index-1
        else:
            arabic_name_index=None
            name_in_arabic="Not Found"
        if arabic_name_index != None:
            arabic_name=content[arabic_name_index]
            index_arabic_name=arabic_name.find(':')
            name_in_arabic=arabic_name[index_arabic_name+1:]
            name_in_arabic=str(name_in_arabic)
            if '\n' in name_in_arabic:
                name_in_arabic=name_in_arabic.replace('\n','')
            if '\u200e' in name_in_arabic:
                name_in_arabic=name_in_arabic.replace('\u200e','')

        if only_arabic_chars(content[nat_index-1]):
            arabic_nationality_index=nat_index-1
        else:
            arabic_nationality_index=None
            nationality_in_arabic='Not Found'
        if arabic_nationality_index != None:
            arabic_nationality=content[arabic_nationality_index]
            index_arabic_nationality=arabic_nationality.find(':')
            nationality_in_arabic=arabic_nationality[index_arabic_nationality+1:]
            nationality_in_arabic=str(nationality_in_arabic)
            if '\n' in nationality_in_arabic:
                nationality_in_arabic=nationality_in_arabic.replace('\n','')
            if '\u200e' in nationality_in_arabic:
                nationality_in_arabic=nationality_in_arabic.replace('\u200e','')
        return name_in_arabic,nationality_in_arabic


def arabic(filename):
    
    try:
        cif_no = filename.split('_')[-1].split('.')[0]
    except:
        cif_no = str(np.random.randint(1000000,2000000))
    
    flag=is_grey_scale(filename)
    if flag==True:
        name,nationality=extract_arabic(filename)
    else:
        textcleaner(filename)
        time.sleep(2)
        name,nationality=extract_arabic('cleaned.jpg')
    return cif_no,name,nationality

        

def emi_extract(text2):  
    text2=list(text2)
    print(text2)
    print(len(text2))
    if len(text2) > 90:  
        del text2[50:50+len(text2)-90]
    if len(text2)<90:
        text2[50]=(len(text2)-88)*'<'
    print(len(text2))
    text2="".join(text2)
    Data= {'Name':None,'Card Number':None,'ID Number':None,'Date Of Birth':None,'Expiry Date':None,'Nationality':None,'Sex':None}
    Data['Card Number']=text2[5:14]
    Data['ID Number']=text2[15:30]
    year_store=text2[30:32]
    birth_month=text2[32:34]
    birth_date=text2[34:36]
    if int(year_store) > 30:
        year='19'+year_store
    else:
        year='20'+year_store

    birth_day=birth_date+'/'+birth_month+'/'+year
    Data["Date Of Birth"]=birth_day 
    Data['Sex']=text2[37]
    expiry_year='20'+text2[38:40]
    expiry_month=text2[40:42]
    expiry_date=text2[42:44]
    Data["Expiry Date"]=expiry_date+'/'+expiry_month+'/'+expiry_year
    Data["Nationality"]=text2[45:48]
    last_line=text2[60:]
    index=last_line.find('<')
    last_name=last_line[0:index]
    next_string=last_line[index+2:]
    index2=next_string.find('<')
    first_name=next_string[0:index2]
    char_list=['K','<']


    non_existent_name_index=list()
    last_string=last_line[index+2+index2+1:]
    for char in last_string:
        if not char in char_list:
            non_existent_name_index.append(next_string.find(char))
    #print(last_string)
    index3=last_string.find('<')
    middle_name=last_string[0:index3]
    name=first_name+' '+middle_name+' '+last_name
    Data['Name']=name
    count=0
    for key in Data.keys():
        if Data[key]=='':
            count+=1
    if count > 5:
        print("Please rescan the document porperly with higher DPI settings")
        return None
    else:    
        return Data

