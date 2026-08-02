import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

root = tk.Tk()
root.geometry("500x600")
root.title("Khaos - Workout Tracker")
root.configure(bg="black")

header_frame = tk.Frame(root, bg="black", height=250)
header_frame.pack(fill="x", padx=5, pady=5)

# Stops the header frame from shrinking
header_frame.pack_propagate(False)

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
    error_label = tk.Label(
        header_frame,
        text="Khaos_Logo.png could not be found.",
        font=("Arial", 18),
        bg="black",
        fg="red"
    )
    error_label.pack(side="left", anchor="n")

text_frame = tk.Frame(header_frame, bg="black")

text_frame.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)

title_label = tk.Label(
    text_frame,
    text="Khaos",
    font=("Arial", 40, "bold"),
    bg="black",
    fg="white"
)
title_label.pack(pady=(0, 65))

subtitle_label = tk.Label(
    text_frame,
    text="Measure The Mayhem",
    font=("Arial", 25, "bold"),
    bg="black",
    fg="white"
)
subtitle_label.pack()

root.mainloop()