#!/usr/bin/env python3
import requests
from PIL import Image
import pytesseract
import cv2
import os

import ScreenshotMetadata
import OCRParsing

def receive(message):
    return_message = "received message, but no image"
    if (len(message.embeds) > 0):
        embed = message.embeds[0]
        #print("url: " + str(embed.image.url))
        return embed.image.url
    if (len(message.attachments) > 0):
        url = message.attachments[0].get('url')
        return_message = url
    return return_message

def download_image(url):
    print("Downloading image: " + url)
    r = requests.get(url)
    index = url.rfind("/") + 1
    name = url[index:]
    with open(name, 'wb') as f:
        f.write(r.content)
    #convert_png_to_jpg('image.png')
    print("Done downloading image: " + url + "\nSaved as " + name)
    return name

def convert_png_to_jpg(png_filename):
    img = Image.open(png_filename)
    jpg = img.convert('RGB')
    jpg.save(png_filename[:-3] + 'jpg')

def ocr(img):
    dpi_image = Image.open(img)
    filename = img[:-3] + '-ocr.png'
    width, height = dpi_image.size
    if (width < 500 or height < 500):
        dpi_image = dpi_image.resize((width*3, height*3), Image.ANTIALIAS)
    dpi_image = dpi_image.crop((width*.28, height*.2, width*.81, height*.91))
    dpi_image.save(filename, dpi=(600,600))

    image = cv2.imread(filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 3)

    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    return text

def parse_ocr(ocr_text):
    ocr_text_split = ocr_text.split()
    seen_coords = False
    mh_list = []
    metadata = ScreenshotMetadata.ScreenshotMetadata()
    for i in range(len(ocr_text_split)):
        pass
    ocr_text_string = " ".join(ocr_text_split)
    valid_hunts = OCRParsing.get_valid_hunts(ocr_text_string)
    return valid_hunts
