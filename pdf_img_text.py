#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 11:38:19 2018

@author: bromount
"""

"""
This script uses the Vision API's text detection capabilities to find a text
based on an image's content.

To run the example, install the necessary libraries by running:

    pip install -r requirements.txt
"""

import argparse
import os

from utils import Service, encode_image
from PyPDF2 import PdfFileWriter, PdfFileReader
from wand.image import Image
from wand.color import Color

def main(photo_file):
    """Run a text detection request on a single image"""

    access_token = os.environ.get('VISION_API')
    if access_token == 'None':
        print "Import VISION API KEY"
    service = Service('vision', 'v1', access_token=access_token)
    with open(photo_file, 'rb') as image:
        base64_image = encode_image(image)
        body = {
            'requests': [{
                'image': {
                    'content': base64_image,
                },
                'features': [{
                    'type': 'TEXT_DETECTION',
                    'maxResults': 1,
                }]

            }]
        }
        response = service.execute(body=body)
        text = response['responses'][0]['textAnnotations'][0]['description']
        print('Found text: {}'.format(text))
        file1=open("./text/pdf_to_text.txt","a")
        #file1.write(text,'\n')
        file1.write("{}\n".format(text))
        file1.close()
        print "Text File modified"

#Getting Input from user

doc_path=raw_input("Enter the file path with file name : ")

inputpdf = PdfFileReader(open(doc_path, "rb"))

for i in range(inputpdf.numPages):
    output = PdfFileWriter()
    output.addPage(inputpdf.getPage(i))
    with open("./pdf/document-page%s.pdf" % i, "wb") as outputStream:
        output.write(outputStream)
        print "Page %s saved" % i
        # Converting pages into JPG
    with Image(filename="./pdf/document-page%s.pdf" % i) as img:
        img.compression_quality = -500
        img.background_color = Color("white")
        img.alpha_channel = 'remove'
        img.save(filename="./image/pdf_image%s.jpg" % i)
        print "Image %s saved" % i
        image_file = "./image/pdf_image%s.jpg" %i
        #print image_file
        main(image_file)
