import tkinter as tk


def blank():
    print("Blank Thread Started")
    blank = tk.Tk()
    width,height=1920,1080 # set the variables 
    d=str(width)+"x"+str(height)
    width,height=1920,1080 # set the variables
    blank.geometry(d)
    blank.configure(bg='#000000')
    blank.title("Blank")
    blank.attributes("-fullscreen", True)
    blank.mainloop()
    pw("Blank Thread Complete")

blank()
