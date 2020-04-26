import tkinter as tk

counter = 0

def onReturn(event):
    global counter
    counter = counter + 1
    print ("a", counter)

    value = entry1.get()
    # print(value)
    entry1.delete(0,'end')

root = tk.Tk()
root.title("GUI entry with return")

entry1 = tk.Entry(root)

entry1.bind("<a>",onReturn)
entry1.pack()

root.mainloop()