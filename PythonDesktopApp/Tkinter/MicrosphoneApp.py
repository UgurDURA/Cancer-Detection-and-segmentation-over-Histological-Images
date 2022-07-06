from tkinter import *
from PIL import ImageTk, Image
import cv2 as cv2

root = Tk()
root.title("MicrosPhone")
img = Image.open("sendImage.png")
img = img.rotate(270)
img = img.resize((750,1000))
 

my_image = ImageTk.PhotoImage(img)
my_label = Label(image=my_image)
my_label.grid(row=1, column=1, columnspan=3)

b_capture = Button(root, text = "Capture")
b_exit = Button(root, text= "Exit", command=root.quit)
b_zoom_in = Button(root, text="+")
b_zoom_out = Button(root, text="-")


b_capture.grid(row=1,column=0)
b_zoom_in.grid(row=2,column=0)
b_zoom_out.grid(row=3,column=0)
b_exit.grid(row=4,column=0)



 

root.mainloop()