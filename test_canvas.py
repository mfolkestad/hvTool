
import tkinter as tk
import cv2
import os 
from PIL import Image, ImageTk
from pathlib import Path

# User input 
workDir = "testImg"
scaleParam = 0.2
default = "0"

# Directory stuff 
while Path(workDir).exists() == False:
    print("No such dir, try again: ")
    workDir = input("Enter dir: ")

os.chdir(workDir)

filename = workDir + ".csv"
outfile = Path.cwd().parent / filename

# Image files 
im_files = [f for f in os.listdir(".") if f[-3:] == 'jpg']
images = iter(im_files)
n_img = str(len(im_files))
count = 0

def next_img(setCounterBack = False):
    try:
        global imgfile
        label.imgtk = imgtk
        label.configure(image=imgtk)
        T.delete(1.0, tk.END)
        T.insert(1.0, imgfile)
        T.config(width = len(imgfile))
        global count
        count += 1
        counter_str = str(count) + "/" + n_img
        counter.delete(1.0,tk.END)
        counter.insert(1.0,counter_str)
        counter.config(width = len(counter_str))
    except StopIteration:
        top.destroy()

imgfile = next(images)  # get the next image from the iterator
with open(outfile, "a") as f:
    f.write(imgfile + ";")
image = cv2.imread(imgfile, flags=cv2.IMREAD_GRAYSCALE)
image = cv2.resize(image, (0, 0), fx = scaleParam, fy = scaleParam) # Update to fit the screen
img = Image.fromarray(image)


# tkinter stuff 
top = tk.Tk()
canvas = tk.Canvas(top, width=100, height=200, background='gray75')

top.mainloop()

