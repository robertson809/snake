import tkinter as tk
from time import sleep

def clear_frame():
   for widgets in frame.winfo_children():
      widgets.destroy()

window = tk.Tk()
frame = tk.Frame(master=window, width=150, height=150)
frame.pack()

for i in range(150):
    label1 = tk.Label(master=frame, text="S", bg="red")
    label1.place(x=i, y=i)

    window.update()
    clear_frame()

for i in range(150,-1,-1):
    label1 = tk.Label(master=frame, text="S", bg="red")
    label1.place(x=i, y=i)

    window.update()
    clear_frame()


window.mainloop()