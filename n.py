import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
import sqlite3

def create_database():
    conn = sqlite3.connect('khaos.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
    )""")

    cursor.execute("""
    INSERT OR IGNORE INTO users (username, password) VALUES
    ('user1', 'pass123'),
    ('user2', 'pass456'),
    ('user3', 'pass789')
    """)

    conn.commit()
    conn.close()


create_database()

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
    login_frame.pack_forget()
    register_frame.pack_forget()
    
    if page_name == "login":
        login_frame.pack(fill="both", expand=True, padx=5, pady=5)
        subtitle_label.config(text="log in /sign up")
        
    elif page_name == "register":
        register_frame.pack(fill="both", expand=True, padx=5, pady=5)
        subtitle_label.config(text="Register")
        
    else:
        login_frame.pack_forget()
        subtitle_label.config(text=f"you have selceted {page_name}")
    


    ########################################################## Main Menu Button ##########################################################
navigation_frame = tk.Frame(root, bg="black", height=50)
navigation_frame.pack(fill="x", padx=5, pady=5)

for i in range(5):
    navigation_frame.grid_columnconfigure(i, weight=1)
    
    
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
    padx=5,
    pady=5,
    ipady=12,
    sticky="nsew"
)


########################################################## Login Frame ##########################################################



login_frame = tk.Frame(root, bg="black")

no_account_label = tk.Label(
    login_frame,
    text="No account?",
    font=("Arial", 11),
    bg="black",
    fg="white"
)
no_account_label.pack(pady=(15, 0))

register_link = tk.Label(
    login_frame,
    text="Register here",
    font=("Arial", 11, "underline"),
    bg="black",
    fg="white",
    cursor="hand2"
)
register_link.pack(pady=(0, 10))

register_link.bind(
    "<Button-1>",
    lambda event: change_page("register")
)


username_label = tk.Label(login_frame, text="Username:", font=( "Arial", 12), bg="black", fg="white")
username_label.pack(pady=(20, 5))

username_entry = tk.Entry(login_frame, font=("Arial", 12))
username_entry.pack(pady=5)

password_label = tk.Label(login_frame, text="Password:", font=( "Arial", 12), bg="black", fg="white")
password_label.pack(pady=(10, 5))

password_entry = tk.Entry(login_frame, font=("Arial", 12))
password_entry.pack(pady=5)

message_label = tk.Label(login_frame, text="", font=("Arial", 11), bg="black", fg="white")
message_label.pack(pady=10)




register_frame = tk.Frame(root, bg="black")

register_label = tk.Label(
    register_frame,
    text="Create an Account",
    font=("Arial", 18, "bold"),
    bg="black",
    fg="white"
)
register_label.pack(pady=(20, 15))

register_username_label = tk.Label(
    register_frame,
    text="Username:",
    font=("Arial", 12),
    bg="black",
    fg="white"
)
register_username_label.pack(pady=(5, 5))

register_username_entry = tk.Entry(
    register_frame,
    font=("Arial", 12)
)
register_username_entry.pack(pady=5)

register_password_label = tk.Label(
    register_frame,
    text="Password:",
    font=("Arial", 12),
    bg="black",
    fg="white"
)
register_password_label.pack(pady=(10, 5))

register_password_entry = tk.Entry(
    register_frame,
    font=("Arial", 12)
)
register_password_entry.pack(pady=5)

register_message_label = tk.Label(
    register_frame,
    text="",
    font=("Arial", 11),
    bg="black",
    fg="white"
)
register_message_label.pack(pady=10)


def register():
    for widget in register_frame.winfo_children():
        widget.destroy()
    username = register_username_entry.get()
    password = register_password_entry.get()

    conn = sqlite3.connect('khaos.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()

        register_message_label.config(
            text="registration successful!")

    except sqlite3.IntegrityError:
        register_message_label.config(
            text="username alarady exists.",
            fg="red"
        )

    conn.close()


register_button = tk.Button(register_frame,text="Register",font=("Arial", 11, "bold"),
                            bg="#202020",fg="white",relief="flat",bd=0,cursor="hand2",command=register)
register_button.pack(pady=10)













def login():
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect('khaos.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()

    conn.close()

    if result:
        message_label.config(text="Login successful!", fg="green")
    else:
        message_label.config(text="Invalid username or password.", fg="red")


submit_button = tk.Button(
    login_frame,
    text="Log In",
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
    command=login
)
submit_button.pack(pady=10)


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

my_workout_button.grid( row=0,column=1,padx=5,pady=5,ipady=12,sticky="nsew")



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

workout_tracker_button.grid(row=0,column=2,padx=5,pady=5,ipady=12,sticky="nsew")

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

exercise_library_button.grid(row=0,column=3,padx=5,pady=5,ipady=12,sticky="nsew")

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

login_button.grid(row=0,column=4,padx=5,pady=5,ipady=12,sticky="nsew")

########################################################## Divider ##########################################################

divider = tk.Frame(root, bg="white", height=5)
divider.pack(fill="x", padx=8, pady=(0, 8))

root.mainloop()