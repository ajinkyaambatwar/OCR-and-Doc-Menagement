from file_max import file_handler

def indianpassport(filename):
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
    Data= {'Name':None,'Passport Number':None,'ID Number':None,'Date Of Birth':None,'Expiry Date':None,'Nationality':None,'Sex':None}
    '''text=pytesseract.image_to_string(img2)
    text=text.replace(" ",'')
    text2=text.replace('\n','')
    '''
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
    Data["Passport Number"]=text2[44:52]

    #---Nationality
    Data["Nationality"]=text2[54:57]

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
    return Data

data=indianpassport('s4-shripad_passport.png')
print(data)
