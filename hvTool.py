from telnetlib import DM
import tkinter as tk
import cv2
import os 
from PIL import Image, ImageTk
from pathlib import Path 
import re  

# User input 
name = input("Your name: ")
name = name.replace(" ","")
date = input("Date: ")
date = date.replace(" ","")
workDir = input("Enter dir: ")
scaleParam = input("Scale Parameter for Img: ")
default = input("Choose default value: ")
scaleParam = float(scaleParam)/100
nEntries = float(input("Entries per img: "))

# Directory stuff 
while Path(workDir).exists() == False:
    print("No such dir, try again: ")
    workDir = input("Enter dir: ")

while nEntries > 2:
    print("Max 2 entries per img: ")
    nEntries = float(input("Entries per img: "))

os.chdir(workDir)

filename = workDir + "_" + name + "_" + date + ".csv"
outfile = Path.cwd().parent / filename

# Image files 
im_files = [f for f in os.listdir(".") if f[-3:] == 'jpg']
images = iter(im_files)
n_img = str(len(im_files))
count = 0

def set_scale():
    w.lower(belowThis=label)
    sp.focus()
    try:
        testImg = im_files[0]
        image = cv2.imread(testImg, flags=cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (0, 0), fx = scaleParam, fy = scaleParam) # Update to fit the screen
        img = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        T.delete(1.0, tk.END)
        T.insert(1.0, "Set scale param")
    except:
        top.destroy()

def next_img(setCounterBack=False):
    try:
        global imgfile
        imgfile = next(images)  # get the next image from the iterator
        with open(outfile, "a") as f:
            f.write(imgfile + ";")
        image = cv2.imread(imgfile, flags=cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (0, 0), fx = scaleParam, fy = scaleParam) # Update to fit the screen
        img = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        T.delete(1.0, tk.END)
        T.insert(1.0, imgfile)
        T.config(width = len(imgfile))
        global count
        if setCounterBack:
            count -=2        
        count += 1
        counter_str = str(count) + "/" + n_img
        counter.delete(1.0,tk.END)
        counter.insert(1.0,counter_str)
        counter.config(width = len(counter_str))
    except StopIteration:
        top.destroy()
    
def func2entries(event, default=default):
    with open(outfile, "r") as f:
        lastRow = f.readlines()[-1]
        entries = sum([bool(i) for i in re.split("(?<=[\;])", lastRow)]) - 1 
    if not entries:
        entry = w.get()
        if entry == "":
            entry = default 
        with open(outfile, "a") as f:
            f.write(entry + ";")
        w.delete(0,"end")
    else:
        entry = w.get()
        if entry == "":
            entry = default 
        with open(outfile, "a") as f:
            f.write(entry + "\n")
        w.delete(0,"end")
        next_img()

def func1entries(event, default=default):
    entry = w.get()
    if entry == "":
        entry = default 
    with open(outfile, "a") as f:
        f.write(entry + "\n")
    w.delete(0,"end")
    next_img()

def go_back(event):
    #This function should go back and erase the entry in the csv file, and return the iterator to the previous image, and then just do next image function. 
    with open(outfile, "r") as f:
        data = f.readlines()
        data.pop()
        data.pop()
    with open(outfile, "w") as f:
        f.writelines(data)
    i = im_files.index(imgfile) - 1 
    global images
    images = iter(im_files[i:])
    next_img(setCounterBack=True)

def done():
    butt1.lower(belowThis=label)
    butt2.lower(belowThis=label)
    sp.lower(belowThis=label)
    w.lift(aboveThis=label)
    w.focus()
    next_img()

def update():
    global scaleParam
    scaleParam = sp.get()
    scaleParam = float(scaleParam) / 100
    set_scale()


# tkinter stuff 
top = tk.Tk()
if nEntries == 1:
    top.bind('<Return>', func1entries)
if nEntries == 2:
    top.bind('<Return>', func2entries)
top.bind("<Left>", go_back)

label = tk.Label(top)
label.pack()

# Text box
T = tk.Text(top, font=('calibre',15,'normal'), fg = "red" , height=1) 
T.place(relx = 0.1, rely = 0.1) # PLACE THE FILENAME BOX

# Counter
counter = tk.Text(top, font=('calibre',15,'normal'), fg = "red" , height=1)
counter.place(anchor=tk.NW) # PLACE THE FILENAME BOX

# Entry box 
w = tk.Entry(top, takefocus=True, font=('calibre',15,'normal'))
w.place(relx = 0.2, rely = 0.9) # PLACE THE ENTRY BOX

# Entry box For scale parameter
sp = tk.Entry(top , font=('calibre',20,'normal'), width=4 )
sp.place(relx = 0.4, rely = 0.4)

butt1 = tk.Button(text = "Done", command = done, width= 4)
butt1.place(relx=0.2, rely=0.8)

butt2 = tk.Button(text = "Rescale", command = update, width= 4)
butt2.place(relx=0.2, rely=0.4)

set_scale()

top.mainloop()

