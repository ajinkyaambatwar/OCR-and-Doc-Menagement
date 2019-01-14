import pytesseract
from PIL import Image
import time
from word_search import file_process

text=pytesseract.image_to_string(Image.open('emirates_id_8.jpg'),'ara+eng')
with open('aratext.txt','w') as file:
    file.writelines(text)
time.sleep(0.5)
content=file_process('engara.txt')
print(content)

for line in content:
    if "Name" in line:
        name_index=content.index(line)

for line in content:
    if "Nationality" in line:
        nat_index=content.index(line)

arabic_name_index=name_index-2
print('hi')
arabic_name=content[arabic_name_index]
index_arabic_name=arabic_name.find(':')
name_in_arabic=arabic_name[index_arabic_name+1:]
print(name_in_arabic)

arabic_nationality_index=nat_index-1
print(content[arabic_nationality_index])

