from tkinter import *
from scanner import takeit
#GLOBAL VARIABLES

#windows & widgets
window = Tk()
window.configure(background="#990033")
window.title("Scanner")
window.geometry("1080x1080")
window.resizable(600,600)
window.iconbitmap("favi.png")
x=1040
y=720
mainframe = Frame(window,padx=5, pady=5,width=x,height=y, bg="#003366")
mainframe.grid(padx=20, pady=20) #pads the frame
mainframe.grid_propagate(False)
for i in range(10):
    mainframe.grid_rowconfigure(i, weight=1)
    mainframe.grid_columnconfigure(i, weight=1)

title = Label(mainframe, text="Welcome to Scanner")
title.grid(row=0, column=4)

line = Entry(mainframe)
line.grid(row=2, column=4)

result = Label(mainframe, text="")
result.grid(row=6, column = 4)

def sub():
    thing=line.get()
    #line.config(state="disabled")
    #submit.config(state="disabled")
    output=takeit(thing.lower())
    result.config(text = output)
    
submit = Button(mainframe, text="Submit line", command = sub)
submit.grid(row=4, column = 4)

window.eval('tk::PlaceWindow . center')
window.mainloop()

#SCENES