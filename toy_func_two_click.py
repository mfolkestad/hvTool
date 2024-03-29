from telnetlib import DM
import tkinter as tk
import cv2
import os 
from PIL import Image, ImageTk
from pathlib import Path
import re  

# User input 
workDir = input("Enter dir: ")
nEntries = float(input("Entries per img: "))
scaleParam = 0.2
default = "0"

# Directory stuff 
while Path(workDir).exists() == False:
    print("No such dir, try again: ")
    workDir = input("Enter dir: ")

while nEntries > 2:
    print("Max 2 entries per img: ")
    nEntries = float(input("Entries per img: "))

os.chdir(workDir)

filename = workDir + ".csv"
outfile = Path.cwd().parent / filename

# Image files 
im_files = [f for f in os.listdir(".") if f[-3:] == 'jpg']
images = iter(im_files)

def next_img():
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
    next_img()

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
T = tk.Text(top, font=('calibre',25,'normal'), fg = "red" , height=1, width=20) #UPDATE FONT SIZE IF NECESSARY
T.place(relx = 0.3, rely = 0.1) # PLACE THE FILENAME BOX

# Entry box 
w = tk.Entry(top, takefocus=True, font=('calibre',32,'normal'), width=10) #UPDATE FONT SIZE IF NECESSARY
w.place(relx = 0.2, rely = 0.9) # PLACE THE ENTRY BOX
w.focus()

next_img()

top.mainloop()

