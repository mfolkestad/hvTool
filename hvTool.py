import tkinter as tk
import cv2
import os 
from PIL import Image, ImageTk
from pathlib import Path 

# User input 
name = input("Your name: ")
name = name.replace(" ","")
date = input("Date: ")
date = date.replace(" ","")
workDir = input("Enter dir: ")
scaleParam = input("Scale Parameter for Img: ")
scaleParam = float(scaleParam)/100

# Directory stuff 
while Path(workDir).exists() == False:
    print("No such dir, try again: ")
    workDir = input("Enter dir: ")

os.chdir(workDir)

filename = workDir + "_" + name + "_" + date + ".csv"
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
        image = cv2.resize(image, (0, 0), fx = scaleParam, fy = scaleParam) # Uppdate to fit the screen
        img = Image.fromarray(image)
        imgtk = ImageTk.PhotoImage(image=img)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        T.delete(1.0, tk.END)
        T.insert(1.0, imgfile)
    except StopIteration:
        top.destroy()
    
def func(event):
    count = w.get()
    if count == "":
        count = "24" 
    with open(outfile, "a") as f:
        f.write(count + "\n")
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
top.bind('<Return>', func)
top.bind("<Left>", go_back)

label = tk.Label(top)
label.pack()

# Entry box 
w = tk.Entry(top, takefocus=True, font=('calibre',32,'normal'), width=10) #UPDATE FONT SIZE IF NESSECARY
w.place(x=180, y=650) # PLACE THE ENTRY BOX
w.focus()

# Text box
T = tk.Text(top, font=('calibre',25,'normal'), fg = "red" , height=1, width=20) #UPDATE FONT SIZE IF NESSECARY
T.place(x = 180, y = 150) # PLACE THE FILENAME BOX

next_img()

top.mainloop()

