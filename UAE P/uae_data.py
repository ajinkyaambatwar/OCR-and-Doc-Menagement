import pytesseract
from file_max import file_handler
from uae import uae_p_extract,arabic
from check import is_grey_scale
from word_search import file_process
import numpy as np
from PIL import Image

def return_data_uae(filename):
    cif,name,nat=arabic(filename)
    text2=file_handler(filename)
    Data=uae_p_extract(text2)
    if Data != None:
        Data['arabic_name']=name
        Data['cif']=cif
        Data['nationality_arabic']=nat
        return Data

print(return_data_uae('s2-passport.jpg'))
