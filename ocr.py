#!/usr/bin/env python3
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh", help="Type of preprocessing to be done")
args = vars(ap.parse_args())

dpi_image = Image.open(args["image"])
filename = args["image"][:-3] + '-300.png'
width, height = dpi_image.size
if (width < 500 or height < 500):
    dpi_image = dpi_image.resize((width*3, height*3), Image.ANTIALIAS)
dpi_image = dpi_image.crop((width*.28, height*.2, width*.81, height*.95))
dpi_image.save(filename, dpi=(600,600))

#image = cv2.imread(args["image"])
image = cv2.imread(filename)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

if args["preprocess"] == "thresh":
    #pass
    #gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #gray = cv2.resize(gray, (1000, 120), interpolation = cv2.INTER_LINEAR)
    #gray = cv2.resize(gray, None, fx=.5, fy=.5)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 3)
    #gray2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 1)
    #gray = cv2.GaussianBlur(gray, (5,5), 0)
    #gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    #gray = cv2.addWeighted(gray1, .7, gray2, .3, 0.0)
    #ret, grayOtsu = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    #gray = cv2.GaussianBlur(gray1, (3, 3), 0)


elif args["preprocess"] == "blur":
    gray = cv2.medianBlur(gray, 3)

filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

text = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
print(text.split())

cv2.imshow("Image", image)
cv2.imshow("Output", gray)
cv2.waitKey(0)


def blend_transparent(face_img, overlay_t_img):
    overlay_img = overlay_t_img[:,:,:3]
    overlay_mask = overlay_t_img[:,:,3:]
    background_mask = 255 - overlay_mask
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvColor(background_mask, cv2.COLOR_GRAY2BGR)
    face_part = (face_img * (1/255.0)) * (background_mask * (1/255.0))
    overlay_part = (overlay_img * (1/255.0)) * (overlay_mask * (1/255.0))
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))
