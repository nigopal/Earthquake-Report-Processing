# Python program to illustrate HoughLine 
# method for line detection 
import cv2 
import numpy as np 
import argparse
import os
import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--folder", required=True,
	help="path for input files")
ap.add_argument("-o", "--output", required=True,
	help="path for output files")
ap.add_argument("-c", "--csv", required=True,
        help='csv of how to crop the images')
# "FIELD, TOPLEFTX, TOPLEFTY, BOTTOM_RIGHTX, BOTTOMRIGHTY" is the intended format
# of the CSV
args = vars(ap.parse_args())

dirname = os.path.dirname(__file__)
inputs = os.path.join(dirname, args["folder"])
outputs = os.path.join(dirname, args["output"])
crop_file = open(os.path.join(dirname, args["csv"]))
crops = pd.read_csv(crop_file)
crops['top_left_x'] = crops['top_left_x'].astype(np.float32)
crops['top_left_y'] = crops['top_left_y'].astype(np.float32)
crops['bottom_right_x'] = crops['bottom_right_x'].astype(np.float32)
crops['bottom_right_y'] = crops['bottom_right_y'].astype(np.float32)

def crop_image(infile, outfile, top_left_coordinates, bottom_right_coordinates):  
    # Reading the required image in  
    # which operations are to be done.  
    # Make sure that the image is in the same  
    # directory in which this python program is 
    img = cv2.imread(infile)

    # Convert the img to grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 

    # Get the height and width of the image
    img_height, img_width = gray.shape

    # Convert the percent values into pixel coordinates
    top_left_x = int(img_width  * top_left_coordinates[1])
    top_left_y = int(img_height * top_left_coordinates[0])
    bottom_right_x = int(img_width * bottom_right_coordinates[1])
    bottom_right_y = int(img_height * bottom_right_coordinates[0])
    
    gray = gray[top_left_x: bottom_right_x, top_left_y: bottom_right_y]
    cv2.imwrite(outfile, gray)


if not os.path.exists(outputs):
    os.makedirs(outputs)

for filename in os.listdir(inputs):
    for _, crop in crops.iterrows():
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".tif") or filename.endswith(".jpeg"):
            crop_image(os.path.join(inputs, filename), 
                       os.path.join(outputs, crop["field_name"] + filename), 
                       (crop["top_left_x"], crop["top_left_y"]), 
                       (crop["bottom_right_x"], crop["bottom_right_y"]))
        else:
            continue
  
 
