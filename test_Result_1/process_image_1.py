
# coding: utf-8

# In[184]:


import cv2
import matplotlib.pyplot as plt
import subprocess as sp
import numpy as np
import pandas as pd
import imutils
import glob
import os


# In[103]:


def apply_ocr(img_path):
    command = ['tesseract', img_path, 'stdout', '--psm=7']
    return sp.run(command, stdout=sp.PIPE)


# In[195]:


file_list = glob.glob('*.jpg')
file_list.extend(glob.glob('*.png'))


# In[238]:

dict_data=dict()
for file_name in file_list:
#     file_name = 's1-ibrahim_passport.jpg'
    print(file_name)
    img = cv2.imread(file_name)
    img = imutils.resize(img, width=600)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    print(gray.shape)
    w,h = gray.shape
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 6))
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

    for i,c in enumerate(cnts):
        locs.loc[i] = list(cv2.boundingRect(c))
    lines = locs[locs.w >= locs.w.max()-30].sort_values(by='y').reset_index(drop=True)
    
#     plt.figure()
#     plt.imshow(thresh, cmap='gray')
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
        
        name = '{}_rotated_{}.jpg'.format(file_name, i)
        cv2.imwrite(name, rotated)
        text=apply_ocr(name).stdout.decode('utf-8')
        os.remove(name)
        text=text.replace(" ",'')
        text=text.replace("\n\x0c",'')

        data.append(text)
    dict_data[file_name]=data

print(dict_data)
# os.remove('rotated.jpg')


# In[179]:

'''
plt.figure()
plt.imshow(thresh, cmap='gray')


# In[219]:


test = cv2.imread('s2-emirates_id.JPG_rotated_0.jpg')
angle = -1
(h, w) = group.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(test, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_WRAP)
plt.imshow(rotated, cmap='gray')


# In[203]:
''

file_list[2:3]


# In[210]:


box
'''