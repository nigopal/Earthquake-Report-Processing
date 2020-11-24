import cv2
import json
import os
import numpy as np

# blur
def blur(image,amount=5):
    return cv2.medianBlur(image,amount)

# dilation
def dilate(image, mode='C'):
    if mode == 'C':
        kernel = np.ones((2,8),np.uint8)
        return cv2.dilate(image, kernel, iterations = 3)
    elif mode == 'E':
        kernel = np.ones((2,4),np.uint8)
        return cv2.dilate(image, kernel, iterations = 1)

# erosion
def erode(image,mode='V'):
    if mode == 'V':
        kernel = np.ones((4,2),np.uint8)
    elif mode == 'H':
        kernel = np.ones((1,3),np.uint8)
    elif mode == 'S':
        kernel = np.ones((3,3),np.uint8)
        kernel[0][0] = 0
        kernel[0][-1] = 0
        kernel[-1][0] = 0
        kernel[-1][-1] = 0
    return cv2.erode(image, kernel, iterations = 1)

# morph
def morph(image, mode='close', iterations=1):
    if mode == 'close':
        for i in range(iterations):
            threshold_img = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
            return cv2.morphologyEx(threshold_img, cv2.MORPH_CLOSE, kernel)
    elif mode == 'open':
        for i in range(iterations):
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20,1))
            return cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

def find_and_replace_lines(img,show=False):
    # Find edges with hough transform
    if show:
        show_img(img,'base')
    morph_img = dilate(img)
    if show:
        show_img(morph_img,'dilate')
    erode_img = erode(morph_img)
    if show:
        show_img(erode_img,'erode')
    edges = cv2.Canny(erode_img,255/3,255,apertureSize = 3)
    if show:
        show_img(edges,'edges')
    dilate_edges = dilate(edges, mode='E')
    if show:
        show_img(dilate_edges,'dilate edges')
    lines = cv2.HoughLinesP(dilate_edges,0.1,np.pi/180,70,minLineLength=80,maxLineGap=5)
    
    # If lines are detected
    if lines is not None:
        # Make copies of image for later use
        height, width = img.shape
        line_base = np.zeros((height,width),np.uint8)
        img_cpy = img.copy()
        img_mask = img.copy()
        
        # Add lines to separate image
        for line in lines:
            x1,y1,x2,y2 = line[0]
            x1,y1,x2,y2 = x1,y1,x2,y2
            slope = (y2 - y1) / (x2 - x1)
            scale = 3
            x1new = int(x1 - scale)
            x2new = int(x2 + scale)
            y1new = int(y1 - scale*slope)
            y2new = int(y2 + scale*slope)
            cv2.line(line_base,(x1new,y1new),(x2new,y2new),(255,255,255),10)
            cv2.line(img_cpy,(x1new,y1new),(x2new,y2new),(0,225,0),10)
        if show:
            show_img(img_cpy,'lines')
        
        # Create mask for the line image based on location of text in the original
        # Erode and dilate image to mostly isolate text
        img_mask = cv2.bitwise_not(img_mask)
        kernel = np.ones((15,1),np.uint8)
        img_mask = cv2.erode(img_mask, kernel, iterations = 1)
        
        # Reshape kernel for dilation
        kernel = kernel.reshape(-1)
        i = int(len(kernel)/2)
        while i > 0:
            kernel[i] = 0
            i -= 1
        kernel = kernel.reshape(-1,1)
        
        img_mask = cv2.dilate(img_mask, kernel, iterations = 1)
        if show:
            show_img(img_mask,'img_mask')
            show_img(line_base,'line_base')
            
        # Calculate line mask by subtracting the image mask from the line base
        line_mask = cv2.bitwise_and(img_mask, line_base)
        line_mask = cv2.bitwise_not(line_mask)
        masked_lines = cv2.bitwise_and(line_mask, line_base)

        # Remove lines from the original image using the line mask
        img = cv2.bitwise_or(img, masked_lines)
        ret,img = cv2.threshold(img,20,255,cv2.THRESH_BINARY)
        if show:
            show_img(masked_lines,'masked_lines')
            show_img(img,'final')
    # If no lines detected
    else:
        pass
        #print("no lines")
    return img

with open('segment_image.json') as f:
    data = json.load(f)

inputs = data["input"]
outputs = data["output"]
templates = data["templates"]
index = 0

for f in os.listdir(inputs):
    img = cv2.imread(inputs + "/" + f, 0)

    while os.path.exists(outputs + f"/image_{index}"):
        index += 1
    os.makedirs(outputs + f"/image_{index}")

    for segment in data["schema"]:
        template = cv2.imread(templates + "/" + segment["input"], 0)
        w, h = template.shape[::-1]

        top = segment["top"]
        bottom = segment["bottom"]
        left = segment["left"]
        right = segment["right"]

        res = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        bottom_right = (min_loc[0] + w, min_loc[1] + h)
        center = (int((min_loc[0] + bottom_right[0]) / 2), int((min_loc[1] + bottom_right[1]) / 2))
        out = img[center[1] - top : center[1] + bottom, center[0] - left : center[0] + right]
        out = find_and_replace_lines(out)
        #out = erode(out, mode='H')
        #out = blur(out)
        #out = morph(out, mode='close', iterations=1)

        cv2.imwrite(outputs + f"/image_{index}/" + segment["output"], out)
    
    index += 1