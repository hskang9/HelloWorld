# -*- coding: utf-8 -*-
# import the necessary packages
from PIL import Image
import pytesseract
import cv2
import numpy as np

 
def ocr(num=0):
    
    
    cap = cv2.VideoCapture(0)
    while(cap.isOpened()):
        ret, img = cap.read()
        if ret == True:
            cv2.imwrite('init.png', img)
            break
    
    img = cv2.imread('init.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #laplacian = cv2.Laplacian(img, cv2.CV_64F)
    processed = img
    # gray = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite('test2.png', processed)
    img = Image.open("test2.png")
    img.load()
    str = pytesseract.image_to_string(img, lang='kor')
    print(str)
    text_file = open("Output{}.txt".format(num), "w")
    text_file.write(str)
    text_file.close()
    cap.release()
    return str


if __name__ == '__main__':
    ocr()
