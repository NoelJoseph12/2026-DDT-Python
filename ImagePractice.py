import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

root = tk.Tk()
root.geometry("500x600")
root.title("Khaos - Workout Tracker")
root.configure(bg="black")

# Finds the image in the same folder as this Python file
image_path = Path(__file__).parent / "Khaos_Logo.png"

try:
    img = Image.open(image_path)
    img = img.resize((200, 200))
    logo = ImageTk.PhotoImage(img)

    logo_label = tk.Label(root, image=logo, bg="black")
    logo_label.pack(pady=20)

except FileNotFoundError:
    error_label = tk.Label(
        root,
        text="Khaos_Logo.png could not be found.",
        font=("Arial", 12),
        bg="black",
        fg="red"
    )
    error_label.pack(pady=20)

title_label = tk.Label(
    root,
    text="Khaos",
    font=("Arial", 28, "bold"),
    bg="black",
    fg="white"
)
title_label.pack(padx=20, pady=20)

subtitle_label = tk.Label(
    root,
    text="Measure The Mayhem",
    font=("Arial", 22, "bold"),
    bg="black",
    fg="white"
)
subtitle_label.pack(padx=10, pady=10)

root.mainloop()