import cv2
import subprocess as sp
import numpy as np
import pandas as pd
import imutils
import os
import matplotlib.pyplot as plt
from PIL import Image

def apply_ocr(img_path):
    command = ['tesseract', img_path, 'stdout', '--psm=7']
    return sp.run(command, stdout=sp.PIPE)

def file_handler(filename):    
    img = cv2.imread(filename)
    img = imutils.resize(img, width=600)
    img=cv2.fastNlMeansDenoising(img,None,9,13)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #print(gray.shape)
    w,h = gray.shape
    #This is test
    img=Image.open(filename)
    data_dict=img.info
    #print(data_dict)
    if 'dpi' in data_dict.keys():
        if data_dict['dpi'][0]<100:
            rect_size=(9,6)
        else:
            rect_size=(12,6)
    else:
        rect_size=(9,6)
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, rect_size)
    sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6, 6))

    tophat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)
    gradX = cv2.Sobel(tophat, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=-1)
    gradX = np.absolute(gradX)
    (minVal, maxVal) = (np.min(gradX), np.max(gradX))
    gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))
    gradX = gradX.astype("uint8")
    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
    thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
    locs = pd.DataFrame(columns=['x', 'y', 'w', 'h'])

    plt.figure()
    plt.imshow(tophat)
    plt.figure()
    plt.imshow(thresh, cmap='gray')
    plt.show()

    for i,c in enumerate(cnts):
        locs.loc[i] = list(cv2.boundingRect(c))
    lines = locs[locs.w >= locs.w.max()-30].sort_values(by='y').reset_index(drop=True)
    
    data=list()
    for i, row in lines.iterrows():
        group = gray[row.y-8:row.y+row.h+8, row.x-10:row.x+row.w+10]
        group_not = cv2.bitwise_not(group)
        thresh = cv2.threshold(group_not, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        coords = np.column_stack(np.where(thresh>0))
        rect = cv2.minAreaRect(coords)
        angle = rect[-1]
        if angle < -45:
            angle = -(90+angle)
        else:
            angle = -angle
        (h, w) = group.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(group, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_WRAP)
        
        name = '{}_rotated_{}.jpg'.format(filename, i)
        cv2.imwrite(name, rotated)
        text=apply_ocr(name).stdout.decode('utf-8')
        os.remove(name)
        text=text.replace(" ",'')
        text=text.replace("\n\x0c",'')
        data.append(text)
        
    text_final="".join(data)
    if '\n' in text_final:
        text_final=text_final.replace('\n','')
    return text_final

#file_handler('emirates_id_41.jpg')
