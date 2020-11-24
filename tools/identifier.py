# User note, do not close the image window until pressing either y or n to say
# whether or not the image is the form. Unrecognized input results in
# acceptance.

import argparse
import os
import pandas as pd

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


ap = argparse.ArgumentParser()
ap.add_argument("-f", "--folder", required=True,
	help="path for input files")
ap.add_argument("-o", "--output", required=True,
	help="path for output files")
ap.add_argument("-r", "--rejects", required=True,
        help='path for files rejected by filter')
ap.add_argument("-t", "--template", required=True,
        help="template image, it should have approximately the same dpi as the"
        " intended images and should be of the header.") 
ap.add_argument("-v", "--verifyrejects", 
        default="true", help="show images and get input if an image is"
        "suspected to be the wrong format", choices=["true", "false"])
args = vars(ap.parse_args())
dirname = os.path.dirname(__file__)
inputs = os.path.join(dirname, args["folder"])
outputs = os.path.join(dirname, args["output"])
rejects  = os.path.join(dirname, args["rejects"])
template= cv.imread(os.path.join(dirname,args["template"]),
        cv.IMREAD_GRAYSCALE)
verify = args["verifyrejects"] == "true"
w,h = template.shape[::-1]
method = cv.TM_CCOEFF
def human_verify(message, img):
    if not verify:
        return False
    img_h, img_w = img.shape[0:2]
    img = img.copy()
    img = cv.resize(img, (int(img_w/4),int(img_h/4)), interpolation=cv.INTER_AREA)
    cv.imshow(message, img)
    print('Is this an image of a C&G5-680?')
    result = cv.waitKey(0) & 0xFF
    cv.destroyAllWindows()
    return result not in ["n",  "N"]
        

def identify(original, outpath, rejectpath):
    print(original)
    original = cv.imread(original, cv.IMREAD_GRAYSCALE)
    img = original.copy()
    img_w, img_h = img.shape[::-1]
    if img_h*.58 > img_w or img_h *.68 < img_w:
        # Catch bad rotations or odd shaped scans
        result = human_verify("Image size error", original)
        if result:
            cv.imwrite(outpath, original)
            return
        else:
            cv.imwrite(rejectpath, original)
            return
    # Apply template Matching
    res = cv.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    img = cv.rectangle(img,top_left, bottom_right,60, 50)
    if top_left[0] > img_w *.5 or top_left[1] > img_h * .2:
        result = human_verify("Recognized the template outside the expected range", img)
        if result:
            cv.imwrite(outpath,original)
            return
        else:
            cv.imwrite(rejectpath, original)
            return
    cv.imwrite(outpath, original)


for filename in os.listdir(inputs):
    if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".tif") or filename.endswith(".jpeg"):
        identify(os.path.join(inputs, filename), 
                 os.path.join(outputs, filename),
                 os.path.join(rejects, filename)) 
     
 
