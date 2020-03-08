# -*- coding: utf-8 -*-

from tkinter import Tk, PhotoImage, Button, messagebox, Canvas

window = Tk()
canvas = Canvas(window, bg='black', width=300, height=300)
canvas.pack()
man = PhotoImage(file = "spaceManRunning.png")
canvas.create_image(20,20,image=man) 

print(canvas.coords(man))




window.mainloop()