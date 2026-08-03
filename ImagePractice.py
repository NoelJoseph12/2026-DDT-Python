import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path

# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.geometry("500x600")
root.title("Khaos - Workout Tracker")
root.configure(bg="black")

# ---------------- HEADER ----------------

header_frame = tk.Frame(
    root,
    bg="black",
    height=250
)
header_frame.pack(fill="x", padx=5, pady=5)

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

# ---------------- TITLE AREA ----------------

text_frame = tk.Frame(
    header_frame,
    bg="black"
)

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
title_label.pack(pady=(0, 25))

subtitle_label = tk.Label(
    text_frame,
    text="Measure The Mayhem",
    font=("Arial", 25, "bold"),
    bg="black",
    fg="white"
)
subtitle_label.pack()

# ---------------- DIVIDER ----------------

divider = tk.Frame(
    root,
    bg="white",
    height=4
)
divider.pack(fill="x", padx=8, pady=(0, 8))

# ---------------- NAVIGATION BAR ----------------

navigation_frame = tk.Frame(
    root,
    bg="black"
)
navigation_frame.pack(fill="x", padx=8, pady=5)

# Makes every navigation column the same size
for column in range(5):
    navigation_frame.columnconfigure(column, weight=1)

# ---------------- HOVER EFFECTS ----------------

def button_hover(event):
    event.widget.config(
        bg="white",
        fg="black"
    )


def button_leave(event):
    event.widget.config(
        bg="#202020",
        fg="white"
    )


# ---------------- BUTTON FUNCTION ----------------

def create_navigation_button(text, column, page_name):
    button = tk.Button(
        navigation_frame,
        text=text,
        font=("Arial", 11, "bold"),
        bg="#202020",
        fg="white",
        activebackground="white",
        activeforeground="black",
        relief="flat",
        bd=0,
        highlightthickness=2,
        highlightbackground="white",
        highlightcolor="white",
        cursor="hand2",
        command=lambda: change_page(page_name)
    )

    button.grid(
        row=0,
        column=column,
        sticky="nsew",
        padx=5,
        pady=5,
        ipady=12
    )

    button.bind("<Enter>", button_hover)
    button.bind("<Leave>", button_leave)


# ---------------- NAVIGATION BUTTONS ----------------

create_navigation_button(
    "Main Menu",
    0,
    "Main Menu"
)

create_navigation_button(
    "My Workout",
    1,
    "My Workout"
)

create_navigation_button(
    "My Workout\nTracker",
    2,
    "My Workout Tracker"
)

create_navigation_button(
    "Exercise\nLibrary",
    3,
    "Exercise Library"
)

create_navigation_button(
    "Log In /\nSign Up",
    4,
    "Log In/Sign Up"
)

# ---------------- SECOND DIVIDER ----------------

bottom_divider = tk.Frame(
    root,
    bg="white",
    height=4
)
bottom_divider.pack(fill="x", padx=8, pady=(5, 0))

# ---------------- PAGE LABEL ----------------

selected_label = tk.Label(
    root,
    text="You have selected Main Menu",
    font=("Arial", 16, "bold"),
    bg="black",
    fg="white"
)
selected_label.pack(pady=25)


def change_page(page_name):
    selected_label.config(
        text=f"You have selected {page_name}"
    )

# ---------------- START APPLICATION ----------------

root.mainloop()