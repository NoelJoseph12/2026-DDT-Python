import tkinter as tk #Imports the tkinter library into my program and uses a short form of 'tk' for ease.

from tkinter import * #From the tkinter library import *(Everything).

root = tk.Tk() #Creates a main application window. Tk() is the window that contains all the buttons, text boxes etc.
root.geometry("500x600") #Sets the size of the window to 500 pixels wide and 600 pixels tall.
root.title("Khaos - Workout Tracker") #Creates a title for the window application called "Khaos - Workout Tracker".

root.configure(bg="black") #Changes the background color of the window application to black.

title_label = tk.Label(root, text="Khaos", font=('Arial', 28, 'bold'), bg="black", fg="white") #Creates a title label called 'Khaos', while allowing me to edit it to have preferred font, size, colour and weight.
title_label.pack(padx=20, pady=20) #Creates a 20 pixel padding horizontally and vertically around the title label.

subtitle_label = tk.Label(root, text="Measure The Mayhem", font=('Arial', 22, 'bold'), bg="black", fg="white") #Creates a subtitle label called 'Measure The Mayhem', while allowing me to edit it to have preferred font, size, colour and weight.
subtitle_label.pack(padx=10, pady=10) #Creates a 10 pixel padding horizontally and vertically around the subtitle label.

root.mainloop() #Starts the tkinter's event loop, which keeps the window open while waiting for user interaction.
change 1