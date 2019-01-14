from file_max import file_handler
from extract_emirates import emi_extract,arabic
import sys

def return_data_emirates(filename):
    cif,name,nat=arabic(filename)
    text2=file_handler(filename)
    Data=emi_extract(text2)
    if Data != None:
        Data['arabic_name']=name
        Data['cif']=cif
        Data['nationality_arabic']=nat
        return Data

print(return_data_emirates(sys.argv[1]))
