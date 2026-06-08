import tkinter as tk

root = tk.Tk()
root.title("My first GUI app")
root.geometry('300x300')

label = tk.Label(root, text = "Hello", font =('Arial', 16))
label.pack()

def say_hello():
    label.config(text="Button Clicked!")
button = tk.Button(root, text = "Click Me", command = say_hello)
button.pack()

entry = tk.Entry(root)
entry.pack()
def entry_change():
    user_text = entry.get()
    label.config(text=user_text)
button2 = tk.Button(root, text = "Entry Change", command = entry_change)
button2.pack()

root.mainloop()