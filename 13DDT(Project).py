import tkinter as tk #Imports the tkinter library into my program and uses a short form of 'tk' for ease.
from PIL import Image, ImageTk
from pathlib import Path

root = tk.Tk() #Creates a main application window. Tk() is the window that contains all the buttons, text boxes etc.
root.geometry("500x600") #Sets the size of the window to 500 pixels wide and 600 pixels tall.
root.title("Khaos - Workout Tracker") #Creates a title for the window application called "Khaos - Workout Tracker".
root.configure(bg="black") #Changes the background color of the window application to black.

header_frame = tk.Frame(root, bg="black", height=250)
header_frame.pack(fill="x", padx=5, pady=5)

header_frame.pack_propagate(False) #Used AI for this as my versions kept failing.

image_path = Path(__file__).parent / "Khaos_Logo.png"

try:
    img = Image.open(image_path)
    img = img.resize((220, 220))
    logo = ImageTk.PhotoImage(img)

    logo_label = tk.Label(
        header_frame,
        image=logo,
        bg="black"
    )
    logo_label.pack(side="left", anchor="n")

except FileNotFoundError:
    error_label = tk.Label(header_frame, text="Khaos_Logo.png could not be found.", font=("Arial", 18), bg="black", fg="red")
    error_label.pack(side="left", anchor="n")

text_frame = tk.Frame(header_frame, bg="black")
text_frame.place(relx=0.5, rely=0.5, anchor="center")

title_label = tk.Label(text_frame, text="Khaos", font=("Arial", 40, "bold"), bg="black", fg="white")
title_label.pack(pady=(0, 65))

subtitle_label = tk.Label(text_frame, text="Measure The Mayhem", font=("Arial", 25, "bold"), bg="black", fg="white")
subtitle_label.pack()

root.mainloop()