from file_max import file_handler
from word_search import file_process
import pytesseract
from PIL import Image
import os
from check import is_grey_scale
import time
import numpy as np

def textcleaner(img_path):
    os.system('bash textcleaner -g -e stretch -f 25 -o 10 -s 1 ' +img_path+' cleaned.jpg')

def extract_arabic(filename):
    text=pytesseract.image_to_string(Image.open(filename),'ara+eng')
    with open('textfile.txt','w') as file:
        file.writelines(text)
    content=file_process('textfile.txt')
    print(content)
    for line in content:
        if "Name" in line:
            name_index=content.index(line)
        else:
            name_index=None
        if "Nationality" in line:
            nat_index=content.index(line)
        else:
            nat_index=None
        
    if name_index != None:
        arabic_name_index=name_index-1
        arabic_name=content[arabic_name_index]
        index_arabic_name=arabic_name.find(':')
        name_in_arabic=arabic_name[index_arabic_name:]
        name_in_arabic=str(name_in_arabic)
        if '\n' in name_in_arabic:
                name_in_arabic=name_in_arabic.replace('\n','')
        if '\u200e' in name_in_arabic:
                name_in_arabic=name_in_arabic.replace('\u200e','')
    else:
        name_in_arabic=None
    
    if nat_index != None:
        arabic_nationality_index=nat_index-1
        arabic_nationality=content[arabic_nationality_index]
        index_arabic_nationality=arabic_nationality.find(':')
        nationality_in_arabic=arabic_nationality[index_arabic_nationality:]
        nationality_in_arabic=str(nationality_in_arabic)
        if '\n' in nationality_in_arabic:
                nationality_in_arabic=nationality_in_arabic.replace('\n','')
        if '\u200e' in nationality_in_arabic:
                nationality_in_arabic=nationality_in_arabic.replace('\u200e','')
    else:
        nationality_in_arabic=None
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

def uae_p_extract(text2):
    text2=list(text2)
        #print(len(text2))
    if len(text2) > 88:
            del text2[40:40+len(text2)-88]
    if len(text2)<88:
            text2.insert(41,"<")
    print(len(text2))
    text2="".join(text2)
    print(text2)
    Data= {'Name':None,'Passport Number':None,'ID Number':None,'Date Of Birth':None,'Expiry Date':None,'Nationality':None,'Sex':None}

            #----Name----=
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

        #----Passport Number
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
    count=0
    for key in Data.keys():
        if Data[key]=='':
            count+=1
    if count > 5:
        print("Please rescan the document porperly with higher DPI settings")
    else:    
        return Data
