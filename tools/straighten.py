# Python program to illustrate HoughLine 
# method for line detection 
import cv2 
import numpy as np 
import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--folder", required=True,
	help="path for input files")
ap.add_argument("-o", "--output", required=True,
	help="path for output files")
args = vars(ap.parse_args())

dirname = os.path.dirname(__file__)
inputs = os.path.join(dirname, args["folder"])
outputs = os.path.join(dirname, args["output"])

def convert_image(infile, outfile):
    # Reading the required image in  
    # which operations are to be done.  
    # Make sure that the image is in the same  
    # directory in which this python program is 
    img = cv2.imread(infile)

    image = img
    img = img[:int(len(img) / 5),:]
    
    # Convert the img to grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
    gray = cv2.bitwise_not(gray)
    
    # Apply edge detection method on the image 
    edges = cv2.Canny(gray,50,150,apertureSize = 3) 
    
    # This returns an array of r and theta values 
    lines = cv2.HoughLines(edges,1,np.pi/180, 200) 

    angle = 0
    counted = 0
    
    # The below for loop runs till r and theta values  
    # are in the range of the 2d array 
    for line in lines: 
        r, theta = line[0]

        theta = theta * 180 / np.pi
        if theta < 10:
            angle += theta
            counted += 1

        if theta > 170:
            angle += theta - 180
            counted += 1

    if counted == 0:
        counted = 1

    angle /= counted
    print(angle)

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
        flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        
    # All the changes made in the input image are finally 
    # written on a new image houghlines.jpg 
    cv2.imwrite(outfile, rotated)

if not os.path.exists(outputs):
    os.makedirs(outputs)

for filename in os.listdir(inputs):
    if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".tif") or filename.endswith(".jpeg"):
        convert_image(os.path.join(inputs, filename), os.path.join(outputs, filename))
    else:
        continue
  
 