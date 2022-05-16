
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path


# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")
root = Tk()


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1512x982")
window.configure(bg = "#FFFFFF")




canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 982,
    width = 1512,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

serverButton = Button(root, text= "Start Sever",pady=50 )
serverButton.pack()

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    760.0,
    491.0,
    image=image_image_1
)

canvas.create_rectangle(
    46.0,
    901.0,
    259.0,
    968.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    1289.0,
    846.0,
    1387.0,
    925.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    1408.0,
    852.0,
    1500.0,
    924.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    285.0,
    920.0,
    671.0,
    958.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    697.0,
    860.0,
    819.0,
    934.0,
    fill="#000000",
    outline="")
window.resizable(False, False)

window.mainloop()
