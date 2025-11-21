#tools https://www.youtube.com/watch?v=YXPyB4XeYLA
#root window = Tk()
#root.mainloop() --> u know

#label widget = Label(root/window, text="...")
#button widget = Button(root/window, text="...")
#input widget = Entry(root)
#frame = Frame(root, text="smthn, padx=5, pady=5)


#place widget - 2 methods
#pack --> place it in there at first available spot, unsophistocated not great. shove it onto the screen
#widget.pack()

#grid system --> uses rows and collumns
#widget.grid(row=y, column=x)

#rows and columns are relative size by default -->
    #if there's nothing in a column, it wont render the column.
    #if there's something in the column, the column is the size of that something

#widget sizing/optics
#widget(padx=50, pady=50, width=50, height=50, fg="red", bg="ffffff". borderwidth=5)


#buttons exapnded
#button=Button(root, text="", command = *insert function* *no parenthesis*,)

#entry expanded
#use widget.get() to get the input
#widget.insert(0, "Enter your name: ")
