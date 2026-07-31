import tkinter as tk #Imports the tkinter library into my program and uses a short form of 'tk' for ease.
from PIL import Image, ImageTk
from pathlib import Path

root = tk.Tk() #Creates a main application window. Tk() is the window that contains all the buttons, text boxes etc.
root.geometry("500x600") #Sets the size of the window to 500 pixels wide and 600 pixels tall.
root.title("Khaos - Workout Tracker") #Creates a title for the window application called "Khaos - Workout Tracker".
root.configure(bg="black") #Changes the background color of the window application to black.

header_frame = tk.Frame(root, bg="black")
header_frame.pack(fill="x", padx=20, pady=20)

image_path = Path(__file__).parent / "Khaos_Logo.png"

try:

    img = Image.open(image_path)
    img = img.resize((120, 120))
    logo = ImageTk.PhotoImage(img)
    logo_label = tk.Label(header_frame, image=logo, bg="black")
    logo_label.pack(side="left")

except FileNotFoundError:
    error_label = tk.Label(root, text="Khaos_Logo.png could not be found.", font=("Arial", 12), bg="black", fg="red")
    error_label.pack(pady=20)

title_label = tk.Label(root, text="Khaos", font=('Arial', 28, 'bold'), bg="black", fg="white") #Creates a title label called 'Khaos', while allowing me to edit it to have preferred font, size, colour and weight.
title_label.pack(padx=20, pady=20) #Creates a 20 pixel padding horizontally and vertically around the title label.

subtitle_label = tk.Label(root, text="Measure The Mayhem", font=('Arial', 18, 'bold'), bg="black", fg="white") #Creates a subtitle label called 'Measure The Mayhem', while allowing me to edit it to have preferred font, size, colour and weight.
subtitle_label.pack(padx=10, pady=10) #Creates a 10 pixel padding horizontally and vertically around the subtitle label.

root.mainloop() #Starts the tkinter's event loop, which keeps the window open while waiting for user interaction.