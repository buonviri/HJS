import cv2
from pyzbar.pyzbar import decode

img = cv2.imread('10000-EC-004.png')

cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

barcodes = decode(img)
"""
barcodes = decode(img)
for barcode in barcodes:
    data = barcode.data.decode('utf-8')
    print("Barcode Data:", data)
"""
# python.exe -m pip install --upgrade pip
# pip install zbar-py
# pip install opencv-contrib-python pyzbar
