import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
import sqlite3


# def create_database():
#     conn = sqlite3.connect('khaos.db')
#     cursor = conn.cursor()

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#     username TEXT PRIMARY KEY,
#     password TEXT NOT NULL
#     )""")

#     cursor.execute("""
#     INSERT INTO users (username, password) VALUES
#     ('user1', 'pass123'),
#     ('user2', 'pass456'),
#     ('user3', 'pass789')
#     """)

#     conn.commit()
#     conn.close()

########################################################## Main Window ##########################################################


# Creates a main application window. Tk() is the window that contains all the buttons, text boxes etc.
root = tk.Tk()
# Sets the size of the window to 500 pixels wide and 600 pixels tall.
root.geometry("500x600")
# Creates a title for the window application called "Khaos - Workout Tracker".
root.title("Khaos - Workout Tracker")
# Changes the background color of the window application to black.
root.configure(bg="black")

########################################################## Header ##########################################################

# Gives the header a 250 px height and a black background. The header is a frame that contains the logo and the title of the application.
header_frame = tk.Frame(root, bg="black", height=250)
header_frame.pack(fill="x", padx=5, pady=5)

# Used AI for this as my versions kept failing.
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
    error_label = tk.Label(header_frame, text="Khaos_Logo.png could not be found.", font=(
        "Arial", 18), bg="black", fg="red")
    error_label.pack(side="left", anchor="n")

########################################################## Title ##########################################################

text_frame = tk.Frame(header_frame, bg="black")
text_frame.place(relx=0.5, rely=0.5, anchor="center")

title_label = tk.Label(text_frame, text="Khaos", font=(
    "Arial", 40, "bold"), bg="black", fg="white")
title_label.pack(pady=(0, 65))

subtitle_label = tk.Label(text_frame, text="Measure The Mayhem", font=(
    "Arial", 25, "bold"), bg="black", fg="white")
subtitle_label.pack()

########################################################## Buttons ##########################################################


def change_page(page_name):
    subtitle_label.config(
        text=f"You have selected {page_name}"
    )

    ########################################################## Main Menu Button ##########################################################
navigation_frame = tk.Frame(root, bg="black", height=50)
navigation_frame.pack(fill="x", padx=5, pady=5)
main_menu_button = tk.Button(
    navigation_frame,
    text="Main Menu",
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
    command=lambda: change_page("Main Menu")
)

main_menu_button.grid(
    row=0,
    column=0,
    sticky="nsew",
    padx=5,
    pady=5,
    ipady=12
)


def login(self):
    self.root.configure(bg="black")
    self.username_label = tk.Label(
        self.root,
        text="Username:",
        font=("Arial", 12),
        bg="black",
        fg="white"
    )
    username = self.username_entry.get()
    password = self.password_entry.get()

    conn = sqlite3.connect('khaos.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()

    if result:
        self.message_label.config(text="Login successful!", fg="green")
        # Proceed to the next page or functionality
    else:
        self.message_label.config(
            text="Invalid username or password.", fg="red")

    conn.close()


main_menu_button.bind("<Enter>")
main_menu_button.bind("<Leave>")


    ########################################################## My Workout Button ##########################################################

my_workout_button = tk.Button(
navigation_frame,
text="My Workout",
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
command=lambda: change_page("My Workout")
)

my_workout_button.grid(
row=0,
column=1,
sticky="nsew",
padx=5,
pady=5,
ipady=12
)

my_workout_button.bind("<Enter>" )
my_workout_button.bind("<Leave>")


    ########################################################## Workout Tracker Button ##########################################################

workout_tracker_button = tk.Button(
navigation_frame,
text="My Workout\nTracker",
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
command=lambda: change_page("My Workout Tracker")
)

workout_tracker_button.grid(
row=0,
column=2,
sticky="nsew",
padx=5,
pady=5,
ipady=12
)

workout_tracker_button.bind("<Enter>")
workout_tracker_button.bind("<Leave>")


########################################################## Exercise Library Button ##########################################################

exercise_library_button = tk.Button(
navigation_frame,
text="Exercise\nLibrary",
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
command=lambda: change_page("Exercise Library")
)

exercise_library_button.grid(
row=0,
column=3,
sticky="nsew",
padx=5,
pady=5,
ipady=12
)

exercise_library_button.bind("<Enter>")
exercise_library_button.bind("<Leave>")


########################################################## Login Button ##########################################################

login_button = tk.Button(
navigation_frame,
text="Log In /\nSign Up",
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
command=lambda: change_page("login")
)

login_button.grid(
row=0,
column=4,
sticky="nsew",
padx=5,
pady=5,
ipady=12
)

login_button.bind("<Enter>")
login_button.bind("<Leave>")

########################################################## Divider ##########################################################

divider = tk.Frame(root, bg="white", height=5)
divider.pack(fill="x", padx=8, pady=(0, 8))

root.mainloop()
