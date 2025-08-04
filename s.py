import tkinter
from tkinter import messagebox

wi = tkinter.Tk()
wi.title('this is the title')
wi.geometry("400x400")

def on_button_click():
    print('button was cliced')
    my_label.config(text="You clicked the button!")

my_label = tkinter.Label(wi, text="Press the button", font=("Arial", 12))
my_label.pack(pady=20)

button = tkinter.Button(wi, text='press me',command=on_button_click,font=('Arial',20), fg='black')
button.pack(pady=20)
wi.mainloop()
