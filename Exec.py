# -*- coding: utf-8 -*-
from tkinter import *
import os
import time

import matplotlib.pyplot as plt

#-- Get Data Files
def sorting(d):
    splitup = d.split('-')
    return splitup[0], splitup[1], splitup[2]

DataPath = "./Dados/"
Data = os.listdir(DataPath)
for i in range(len(Data)):
    Data[i] = Data[i].split(".")[0]
    
Data = sorted(Data, key=sorting)

#-- Start Window
window = Tk()
window.title("Open Source HFT Trader")
window.configure(bg="grey")
window.geometry('{}x{}'.format(1980, 1080))

#-- Asks Language
win = Toplevel()
win.wm_title("Select language")

width = win.winfo_width()
height = win.winfo_height()
x = (win.winfo_screenwidth() // 2) - (width // 2)
y = (win.winfo_screenheight() // 2) - (height // 2)
win.geometry('{}x{}+{}+{}'.format(400, 100, x, y))
win.attributes('-topmost', 'true')

win.columnconfigure(0, weight=1)

LanguageLabel = Label(win, text="Select Language")
LanguageLabel.grid(row=0, column=0)

Languagevar = StringVar(window)
Languagevar.set("English")

LanguageOps = ["Portugues", "English"]
Language = OptionMenu(win, Languagevar, *LanguageOps)
Language.grid(row=1, column=0, pady=10)

Done = Button(win, text="Done", command=win.destroy)
Done.grid(row=2, column=0)

window.wait_window(win)

#Proceed after language is selected
window.deiconify()

LanguageSelected = Languagevar.get()


if LanguageSelected == "Portugues":
    
    #Import classes
    from bin.InterfacePOR import Menu
    
    #add interface variables
    menu = Menu(Data, DataPath)
    
    menu.Build_Variables(window)
    
    menu.Build_Fields(window)
    
    menu.Graph(window, plt)
    
    mainloop()
    
elif LanguageSelected == "English":
    #Import classes
    from bin.InterfaceING import Menu
    
    #add interface variables
    menu = Menu(Data, DataPath)
    
    menu.Build_Variables(window)
    
    menu.Build_Fields(window)
    
    menu.Graph(window, plt)
    
    mainloop()