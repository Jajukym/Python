import Tkinter as tk
from Tkinter import *

top = Tk() #draw a window

btn1 = Button() #create a button
btn1.pack() #draw button
btn1['text'] = 'Click Me!' #button config

def clicked(): #function of click
    print('I was clicked!')

btn1['command'] = clicked #button config
mainloop()

