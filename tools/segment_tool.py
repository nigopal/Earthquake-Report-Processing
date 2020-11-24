import cv2
import numpy as np

import tkinter as tk

from PIL import Image
from PIL import ImageTk

global path, root, panel, form, top_tk, bottom_tk, left_tk, right_tk, top_sv, bottom_sv, left_sv, right_sv, top, bottom, left, right, img, img_ref, template
global center

path = '../data/form/'
# forms = ['1a.png', '1b.png', '2b.png', '2c.png',
#         '2d.png', '2e.png', '2f.png', '2g.png',
#         '2h.png', '3a.png', '3b.png', '3c.png',
#         '4a.png', '4b.png', '4c.png', '5a.png',
#         '5b.png']

form = '1b.png'

img = cv2.imread(path + 'form.png', 0)
img_ref = img.copy()

template = cv2.imread(path + form, 0)
w, h = template.shape[::-1]

img = img_ref.copy()
res = cv2.matchTemplate(img, template, cv2.TM_SQDIFF_NORMED)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

top = 300
bottom = 300
left = 300
right = 300

top_left = min_loc
bottom_right = (top_left[0] + w, top_left[1] + h)
cv2.rectangle(img,top_left, bottom_right, (255, 0, 0), 2)
center = (int((top_left[0] + bottom_right[0]) / 2), int((top_left[1] + bottom_right[1]) / 2))

root = tk.Tk()

def show_image():
    image = img[center[1] - top : center[1] + bottom, center[0] - left : center[0] + right]
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)

    panel = tk.Label(image=image)
    panel.image = image
    panel.pack(side="left", expand="yes")

    reference = Image.fromarray(template)
    reference = ImageTk.PhotoImage(reference)
    panel2 = tk.Label(image=reference)
    panel2.image=reference
    panel2.pack(side="right", expand="yes")

    top_sv = tk.StringVar()
    bottom_sv = tk.StringVar()
    left_sv = tk.StringVar()
    right_sv = tk.StringVar()
    file_sv = tk.StringVar()

    top_sv.set("300")
    bottom_sv.set("300")
    left_sv.set("300")
    right_sv.set("300")

    def update_image(name, index, mode):
        top = int(top_sv.get())
        bottom = int(bottom_sv.get())
        left = int(left_sv.get())
        right = int(right_sv.get())

        image = img[center[1] - top : center[1] + bottom, center[0] - left : center[0] + right]
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        panel.configure(image=image)
        panel.image = image

    top_sv.trace("w", update_image)
    bottom_sv.trace("w", update_image)
    left_sv.trace("w", update_image)
    right_sv.trace("w", update_image)
    
    right_tk = tk.Entry(root, textvariable=right_sv)
    left_tk = tk.Entry(root, textvariable=left_sv)
    bottom_tk = tk.Entry(root, textvariable=bottom_sv)
    top_tk = tk.Entry(root, textvariable=top_sv)

    right_tk.pack(side="bottom")
    left_tk.pack(side="bottom")
    bottom_tk.pack(side="bottom")
    top_tk.pack(side="bottom")

show_image()

root.mainloop()