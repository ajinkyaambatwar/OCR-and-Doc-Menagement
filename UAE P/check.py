from PIL import Image
import sys
def is_grey_scale(img_path):
    im = Image.open(img_path).convert('RGB')
    w,h = im.size
    for i in range(w):
        for j in range(h):
            r,g,b = im.getpixel((i,j))
            if r != g != b: return False
    im.close()
    return True

#print(is_grey_scale(sys.argv[1]))