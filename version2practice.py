import tkinter as tk  # Imports Tkinter and gives it the shorter name "tk".
from PIL import Image, ImageTk  # Imports tools for opening and displaying images.
from pathlib import Path  # Imports Path to create a reliable path to the logo.
import sqlite3  # Imports SQLite so the program can store user accounts.


# ==========================================================
# DATABASE
# ==========================================================

def create_database():  # Defines a function that creates the user database.
    conn = sqlite3.connect("khaos.db")  # Opens the database or creates it if it does not exist.
    cursor = conn.cursor()  # Creates a cursor used to run SQL commands.

    cursor.execute(  # Runs an SQL command to create the users table.
        "CREATE TABLE IF NOT EXISTS users ("  # Creates the table only if it does not already exist.
        "username TEXT PRIMARY KEY, "  # Creates a unique username column.
        "password TEXT NOT NULL)"  # Creates a password column that cannot be empty.
    )

    cursor.execute(  # Runs an SQL command to add example accounts.
        "INSERT OR IGNORE INTO users (username, password) VALUES "  # Adds users unless they already exist.
        "('user1', 'pass123'), "  # Adds the first example account.
        "('user2', 'pass456'), "  # Adds the second example account.
        "('user3', 'pass789')"  # Adds the third example account.
    )

    conn.commit()  # Saves the database changes.
    conn.close()  # Closes the database connection.


create_database()  # Calls the function when the program starts.


# ==========================================================
# MAIN WINDOW
# ==========================================================

root = tk.Tk()  # Creates the main application window.
root.title("Khaos - Workout Tracker")  # Sets the title shown at the top of the window.
root.state("zoomed")  # Opens the application in a maximised window.
root.configure(bg="black")  # Changes the main window background to black.


# ==========================================================
# LOGIN STATUS
# ==========================================================

logged_in = False  # Records whether a user is currently logged in.
current_user = None  # Stores the username of the logged-in user.
my_workout_exercises = []


# ==========================================================
# EXERCISE DATA
# ==========================================================

EXERCISE_IMAGE_FOLDER = Path(__file__).parent / "exercise_images"

def load_exercise_image(filename, size=(150, 150)):
    if not filename:
        return None
    try:
        img = Image.open(EXERCISE_IMAGE_FOLDER / filename)
        img = img.resize(size)
        return ImageTk.PhotoImage(img)
    except Exception:
        return None

EXERCISE_DATA = [
    {"name": "Barbell Bench Press", "description": "Lower the bar towards your chest, then press it upwards.", "category": "Chest", "image": ""},
    {"name": "Incline Dumbbell Press", "description": "Press dumbbells upwards while lying on an inclined bench.", "category": "Chest", "image": ""},
    {"name": "Machine Chest Fly", "description": "Bring the handles together in front of your chest.", "category": "Chest", "image": ""},
    {"name": "Dips", "description": "Holding onto two parallel bars, lowering your body by bending your arms, and then pushing yourself back up", "category": "Chest", "image": ""},

    {"name": "Dumbbell Shoulder Press", "description": "Press dumbbells upwards from shoulder height.", "category": "Shoulders", "image": ""},
    {"name": "Dumbbell Lateral Raises", "description": "Raise dumbbells out to your sides until they reach shoulder height.", "category": "Shoulders", "image": ""},
    {"name": "Dumbbell Raises", "description": "Lift dumbbells directly in front of your body.", "category": "Shoulders", "image": ""},
    {"name": "Rear Delt Fly", "description": "Bend forward and raise dumbbells out to your sides.", "category": "Shoulders", "image": ""},
    
    {"name": "Preacher Curls", "description": "Curl a weight while resting your upper arms on a preacher bench.", "category": "Biceps", "image": ""},
    {"name": "Incline Dumbbell Curls", "description": "Curl dumbbells while sitting back on an inclined bench.", "category": "Biceps", "image": ""},
    {"name": "Hammer Curls", "description": "Curl dumbbells with your palms facing towards each other.", "category": "Biceps", "image": ""},
    {"name": "Barbell Curls", "description": "Curl a barbell towards your chest without moving your elbows.", "category": "Biceps", "image": ""},
    
    {"name": "Overhead Tricep Extensions", "description": "Lower a weight behind your head, then extend your arms upwards.", "category": "Triceps", "image": ""},
    {"name": "Skull Crushers", "description": "Lower a barbell towards your forehead, then press it upwards.", "category": "Triceps", "image": ""},
    {"name": "Dumbbell Extensions", "description": "Extend dumbbells overhead with straight arms.", "category": "Triceps", "image": ""},
    {"name": "Cable Tricep Pushdown", "description": "Push a cable down towards your thighs.", "category": "Triceps", "image": ""},
    
    {"name": "Lat Pulldowns", "description": "Pull a cable bar down towards your upper chest.", "category": "Back", "image": ""},
    {"name": "Seated Cable Rows", "description": "Pull a cable towards your torso while seated.", "category": "Back", "image": ""},
    {"name": "T-Bar Rows", "description": "Pull a T-bar weight towards your torso.", "category": "Back", "image": ""},
    {"name": "Deadlifts", "description": "Lift a barbell from the ground to hip level.", "category": "Back", "image": ""},
    
    {"name": "Squats", "description": "Stand with feet shoulder-width apart and lower your body by bending your knees and hips.", "category": "Legs", "image": ""},
    {"name": "Romanian Deadlifts", "description": "Lift a barbell from the ground to hip level with a slight bend in your knees.", "category": "Legs", "image": ""},
    {"name": "Calf Raises", "description": "Raise your heels off the ground while standing on your toes.", "category": "Legs", "image": ""},
    {"name": "Leg Extensions", "description": "Extend your legs straight out in front of you while seated.", "category": "Legs", "image": ""},
    {"name": "Leg Press", "description": "Push a weight away from your body while seated.", "category": "Legs", "image": ""},
    {"name": "Leg Curls", "description": " Curl your legs under your body while seated.", "category": "Legs", "image": ""},
    
    {"name": "Machine Abdominal Crunches", "description": "Perform crunches using a machine designed for abdominal exercises.", "category": "Core", "image": ""},
    {"name": "Planks", "description": "Hold a position similar to a push-up, but rest on your forearms.", "category": "Core", "image": ""},
    {"name": "Russian Twists", "description": "Sit on the floor and twist your torso from side to side.", "category": "Core", "image": ""},     
]


# ==========================================================
# HEADER
# ==========================================================

header_frame = tk.Frame(root, bg="black", height=250)  # Creates the frame at the top of the window.
header_frame.pack(fill="x", padx=5, pady=5)  # Places the header across the full width of the window.
header_frame.pack_propagate(False)  # Prevents the frame from changing size to match its contents.

image_path = Path(__file__).parent / "Khaos_Logo.png"  # Finds the logo in the same folder as this Python file.

try:  # Attempts to open and display the logo.
    img = Image.open(image_path)  # Opens the Khaos logo image.
    img = img.resize((220, 220))  # Changes the image size to 220 by 220 pixels.
    logo = ImageTk.PhotoImage(img)  # Converts the image into a format Tkinter can display.

    logo_label = tk.Label(  # Creates a label that will contain the logo.
        header_frame,  # Places the label inside the header.
        image=logo,  # Displays the converted logo.
        bg="black"  # Gives the label a black background.
    )

    logo_label.pack(side="left", anchor="n")  # Positions the logo at the upper-left of the header.

except FileNotFoundError:  # Runs if the logo image cannot be found.
    error_label = tk.Label(  # Creates an error message label.
        header_frame,  # Places the error message inside the header.
        text="Khaos_Logo.png could not be found.",  # Explains which file is missing.
        font=("Arial", 14),  # Sets the font and font size.
        bg="black",  # Gives the label a black background.
        fg="red"  # Makes the error message red.
    )

    error_label.pack(side="left", anchor="n")  # Places the error message at the upper-left.


# ==========================================================
# TITLE
# ==========================================================

text_frame = tk.Frame(header_frame, bg="black")  # Creates a frame for the title and subtitle.
text_frame.place(relx=0.5, rely=0.5, anchor="center")  # Places the text frame in the centre of the header.

title_label = tk.Label(  # Creates the main Khaos title.
    text_frame,  # Places the title inside the text frame.
    text="Khaos",  # Sets the title text.
    font=("Arial", 40, "bold"),  # Makes the title large and bold.
    bg="black",  # Gives the title a black background.
    fg="white"  # Makes the title text white.
)

title_label.pack(pady=(0, 10))  # Displays the title with space underneath it.

subtitle_label = tk.Label(  # Creates the subtitle below the main title.
    text_frame,  # Places the subtitle inside the text frame.
    text="Measure The Mayhem",  # Sets the starting subtitle.
    font=("Arial", 20, "bold"),  # Makes the subtitle bold.
    bg="black",  # Gives the subtitle a black background.
    fg="white"  # Makes the subtitle text white.
)

subtitle_label.pack()  # Displays the subtitle.

# ==========================================================
# DIVIDER
# ==========================================================

divider = tk.Frame(root, bg="white", height=5)  # Creates a white divider above the navigation bar.
divider.pack(fill="x", padx=8, pady=(0, 8))  # Displays the divider across the window.


# ==========================================================
# NAVIGATION FRAME
# ==========================================================

navigation_frame = tk.Frame(root, bg="black", height=60)  # Creates the navigation bar.
navigation_frame.pack(fill="x", padx=5, pady=5)  # Places the navigation bar across the window.


# ==========================================================
# CONTENT AREA
# ==========================================================

content_frame = tk.Frame(root, bg="black")  # Creates the main area where page content will appear.
content_frame.pack(fill="both", expand=True, padx=5, pady=5)  # Makes the content area fill the available space.


# ==========================================================
# CLEAR CONTENT
# ==========================================================

def clear_content():  # Defines a function that removes the current page.
    for widget in content_frame.winfo_children():  # Loops through every widget inside the content frame.
        widget.destroy()  # Deletes the current widget from the screen.


# ==========================================================
# MAIN MENU
# ==========================================================

def show_main_menu():  # Defines the function that displays the main menu.
    clear_content()  # Removes the content from the previous page.

    subtitle_label.config(text="Measure The Mayhem")  # Changes the subtitle back to the original slogan.

    title = tk.Label(  # Creates the main-menu heading.
        content_frame,  # Places the heading inside the content area.
        text="Welcome to Khaos",  # Sets the heading text.
        font=("Arial", 22, "bold"),  # Makes the heading large and bold.
        bg="black",  # Gives the heading a black background.
        fg="white"  # Makes the heading text white.
    )

    title.pack(pady=(25, 10))  # Displays the heading with space around it.

    message = tk.Label(  # Creates an instruction message.
        content_frame,  # Places the message inside the content area.
        text="Your Personal Workout Tracker\nChoose an option from the navigation bar.",  # Tells the user what to do.
        font=("Arial", 12),  # Sets the message font.
        bg="black",  # Gives the message a black background.
        fg="white"  # Makes the message text white.
    )

    message.pack(pady=5)  # Displays the instruction message.


# ==========================================================
# MY WORKOUT
# ==========================================================

def show_my_workout():  # Defines the function that displays the My Workout page.
    if not logged_in:  # Checks whether the user is logged in.
        show_login()  # Sends logged-out users to the login page.
        return  # Stops the rest of this function from running.

    clear_content()  # Removes the content from the previous page.
    subtitle_label.config(text="My Workout")  # Changes the header subtitle.

    title = tk.Label(  # Creates the My Workout heading.
        content_frame,  # Places the heading inside the content area.
        text="My Workout",  # Sets the heading text.
        font=("Arial", 22, "bold"),  # Makes the heading large and bold.
        bg="black",  # Gives the heading a black background.
        fg="white"  # Makes the heading text white.
    )

    title.pack(pady=(25, 15))  # Displays the heading with space around it.

    if not my_workout_exercises:
        message = tk.Label(  # Creates a message for the My Workout page.
            content_frame,  # Places the message inside the content area.
            text="Your saved workouts will appear here.",  # Explains what will be shown on this page.
            font=("Arial", 12),  # Sets the message font.
            bg="black",  # Gives the message a black background.
            fg="white"  # Makes the message text white.
        )

        message.pack(pady=5)  # Displays the message.
        return

    list_frame = tk.Frame(content_frame, bg="black")
    list_frame.pack(fill="both", expand=True, padx=20)

    def remove_exercise(exercise):
        my_workout_exercises.remove(exercise)
        show_my_workout()

    for exercise in my_workout_exercises:
        row = tk.Frame(list_frame, bg="#202020")
        row.pack(fill="x", pady=6)

        info = tk.Frame(row, bg="#202020")
        info.pack(side="left", fill="x", expand=True, padx=12, pady=10)

        tk.Label(
            info, text=exercise["name"], font=("Arial", 12, "bold"),
            bg="#202020", fg="white", anchor="w"
        ).pack(fill="x")

        tk.Label(
            info, text=exercise["category"], font=("Arial", 10),
            bg="#202020", fg="#a9a9a9", anchor="w"
        ).pack(fill="x")

        tk.Button(
            row, text="Remove", font=("Arial", 10, "bold"),
            bg="#7a7a7a", fg="white", activebackground="white", activeforeground="black",
            relief="flat", bd=0, cursor="hand2",
            command=lambda ex=exercise: remove_exercise(ex)
        ).pack(side="right", padx=12, ipady=4)


# ==========================================================
# EXERCISE LIBRARY
# ==========================================================

def show_exercise_library():
    if not logged_in:
        show_login()
        return

    clear_content()
    subtitle_label.config(text="Exercise Library")

    title = tk.Label(
        content_frame,
        text="Exercise Library",
        font=("Arial", 22, "bold"),
        bg="black",
        fg="white",
        anchor="w"
    )

    title.pack(pady=(15, 10), padx=20, fill="x")

    search_placeholder = "Search Exercise"

    search_box = tk.Frame(content_frame, bg="#a9a9a9")
    search_box.pack(fill="x", padx=20, pady=(0, 15))

    search_entry = tk.Entry(
        search_box,
        font=("Arial", 12),
        bg="#a9a9a9",
        fg="white",
        insertbackground="white",
        relief="flat",
        bd=0
    )

    search_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(12, 0))
    search_entry.insert(0, search_placeholder)

    search_icon = tk.Label(
        search_box,
        text="\U0001F50D",
        font=("Arial", 13),
        bg="#a9a9a9",
        fg="white"
    )

    search_icon.pack(side="right", padx=12)

    def clear_placeholder(event):
        if search_entry.get() == search_placeholder:
            search_entry.delete(0, "end")

    def restore_placeholder(event):
        if search_entry.get() == "":
            search_entry.insert(0, search_placeholder)

    search_entry.bind("<FocusIn>", clear_placeholder)
    search_entry.bind("<FocusOut>", restore_placeholder)

    scroll_container = tk.Frame(content_frame, bg="black")
    scroll_container.pack(fill="both", expand=True, padx=20, pady=(0, 15))

    library_canvas = tk.Canvas(scroll_container, bg="black", highlightthickness=0)
    scrollbar = tk.Scrollbar(scroll_container, orient="vertical", command=library_canvas.yview)
    cards_frame = tk.Frame(library_canvas, bg="black")

    cards_frame.bind(
        "<Configure>",
        lambda event: library_canvas.configure(scrollregion=library_canvas.bbox("all"))
    )

    library_canvas.create_window((0, 0), window=cards_frame, anchor="nw")
    library_canvas.configure(yscrollcommand=scrollbar.set)

    library_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def on_mousewheel(event):
        library_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    library_canvas.bind_all("<MouseWheel>", on_mousewheel)

    def open_exercise_details(exercise):
        detail_window = tk.Toplevel(root)
        detail_window.title(exercise["name"])
        detail_window.configure(bg="black")
        detail_window.geometry("400x300")

        tk.Label(
            detail_window, text=exercise["name"], font=("Arial", 18, "bold"),
            bg="black", fg="white"
        ).pack(pady=(20, 5))

        tk.Label(
            detail_window, text=exercise["category"], font=("Arial", 12, "italic"),
            bg="black", fg="#a9a9a9"
        ).pack(pady=(0, 15))

        tk.Label(
            detail_window, text=exercise["description"], font=("Arial", 11),
            bg="black", fg="white", wraplength=350, justify="left"
        ).pack(padx=20)

        tk.Button(
            detail_window, text="Close", font=("Arial", 10, "bold"),
            bg="#202020", fg="white", relief="flat", cursor="hand2",
            command=detail_window.destroy
        ).pack(pady=20)

    def add_exercise_to_workout(exercise, add_button):
        if exercise in my_workout_exercises:
            add_button.config(text="Already Added")
        else:
            my_workout_exercises.append(exercise)
            add_button.config(text="Added!")

        def reset_button():
            if add_button.winfo_exists():
                add_button.config(text="Add Exercise")

        content_frame.after(1200, reset_button)

    def build_card(exercise):
        card = tk.Frame(cards_frame, bg="black")

        tk.Label(
            card, text=exercise["name"], font=("Arial", 11, "bold"),
            bg="black", fg="white", anchor="w"
        ).grid(row=0, column=0, sticky="w")

        tk.Label(
            card, text=exercise["category"], font=("Arial", 11, "bold"),
            bg="black", fg="white", anchor="w"
        ).grid(row=0, column=1, sticky="w", padx=(15, 0))

        photo = load_exercise_image(exercise.get("image"))

        if photo:
            image_label = tk.Label(card, image=photo, bg="black")
            image_label.image = photo
            image_label.grid(row=1, column=0, pady=(6, 0))
        else:
            image_box = tk.Canvas(
                card, width=150, height=150, bg="#c9c9c9", highlightthickness=0
            )
            image_box.grid(row=1, column=0, pady=(6, 0))
            image_box.create_rectangle(1, 1, 149, 149, outline="#8a8a8a")
            image_box.create_line(1, 1, 149, 149, fill="#8a8a8a", dash=(3, 2))
            image_box.create_line(1, 149, 149, 1, fill="#8a8a8a", dash=(3, 2))

        button_frame = tk.Frame(card, bg="black")
        button_frame.grid(row=1, column=1, sticky="n", padx=(15, 0), pady=(20, 0))

        view_button = tk.Button(
            button_frame, text="View Exercise", font=("Arial", 10, "bold"), width=15,
            bg="#7a7a7a", fg="white", activebackground="white", activeforeground="black",
            relief="flat", bd=0, cursor="hand2",
            command=lambda: open_exercise_details(exercise)
        )
        view_button.pack(pady=(0, 10), ipady=6)

        add_button = tk.Button(
            button_frame, text="Add Exercise", font=("Arial", 10, "bold"), width=15,
            bg="#7a7a7a", fg="white", activebackground="white", activeforeground="black",
            relief="flat", bd=0, cursor="hand2"
        )
        add_button.config(command=lambda: add_exercise_to_workout(exercise, add_button))
        add_button.pack(ipady=6)

        return card

    def render_cards():
        for widget in cards_frame.winfo_children():
            widget.destroy()

        typed_text = search_entry.get().strip().lower()
        if typed_text == search_placeholder.lower():
            typed_text = ""

        matches = [
            exercise for exercise in EXERCISE_DATA
            if typed_text in exercise["name"].lower()
            or typed_text in exercise["category"].lower()
        ]

        columns = 3

        if not matches:
            tk.Label(
                cards_frame, text="No exercises found.", font=("Arial", 12),
                bg="black", fg="white"
            ).grid(row=0, column=0, columnspan=columns, pady=30)
            return

        for index, exercise in enumerate(matches):
            row = index // columns
            col = index % columns
            build_card(exercise).grid(row=row, column=col, padx=60, pady=20, sticky="n")

    def on_search_change(event):
        render_cards()

    search_entry.bind("<KeyRelease>", on_search_change)

    render_cards()


# ==========================================================
# LOGIN PAGE
# ==========================================================

def show_login():  # Defines the function that displays the login page.
    clear_content()  # Removes the content from the previous page.
    subtitle_label.config(text="Log In / Sign Up")  # Changes the header subtitle.

    login_frame = tk.Frame(content_frame, bg="black")  # Creates a frame for the login form.
    login_frame.pack(fill="both", expand=True)  # Makes the login frame fill the content area.

    no_account_label = tk.Label(  # Creates the "No account?" message.
        login_frame,  # Places the message inside the login frame.
        text="No account?",  # Sets the message text.
        font=("Arial", 11),  # Sets the message font.
        bg="black",  # Gives the message a black background.
        fg="white"  # Makes the message text white.
    )

    no_account_label.pack(pady=(15, 0))  # Displays the message above the registration link.

    register_link = tk.Label(  # Creates the clickable registration link.
        login_frame,  # Places the link inside the login frame.
        text="Register here",  # Sets the link text.
        font=("Arial", 11, "underline"),  # Underlines the text so it looks like a link.
        bg="black",  # Gives the link a black background.
        fg="white",  # Makes the link text white.
        cursor="hand2"  # Changes the mouse pointer when it moves over the link.
    )

    register_link.pack(pady=(0, 10))  # Displays the registration link.
    register_link.bind("<Button-1>", lambda event: show_register())  # Opens the registration page when clicked.

    username_label = tk.Label(  # Creates the username label.
        login_frame,  # Places the label inside the login frame.
        text="Username:",  # Sets the label text.
        font=("Arial", 12),  # Sets the label font.
        bg="black",  # Gives the label a black background.
        fg="white"  # Makes the label text white.
    )

    username_label.pack(pady=(20, 5))  # Displays the username label.

    global username_entry  # Allows the login function to access the username entry.

    username_entry = tk.Entry(  # Creates the username input box.
        login_frame,  # Places the input box inside the login frame.
        font=("Arial", 12),  # Sets the text font.
        width=25  # Sets the width of the input box.
    )

    username_entry.pack(pady=5)  # Displays the username input box.

    password_label = tk.Label(  # Creates the password label.
        login_frame,  # Places the label inside the login frame.
        text="Password:",  # Sets the label text.
        font=("Arial", 12),  # Sets the label font.
        bg="black",  # Gives the label a black background.
        fg="white"  # Makes the label text white.
    )

    password_label.pack(pady=(10, 5))  # Displays the password label.

    global password_entry  # Allows the login function to access the password entry.

    password_entry = tk.Entry(  # Creates the password input box.
        login_frame,  # Places the input box inside the login frame.
        font=("Arial", 12),  # Sets the text font.
        width=25,  # Sets the width of the input box.
        show="*"  # Replaces the typed password with asterisks.
    )

    password_entry.pack(pady=5)  # Displays the password input box.

    global message_label  # Allows the login function to update the message label.

    message_label = tk.Label(  # Creates a label for login messages.
        login_frame,  # Places the message inside the login frame.
        text="",  # Starts with no message.
        font=("Arial", 11),  # Sets the message font.
        bg="black",  # Gives the message a black background.
        fg="white"  # Makes the starting text white.
    )

    message_label.pack(pady=10)  # Displays the message area.

    submit_button = tk.Button(  # Creates the login button.
        login_frame,  # Places the button inside the login frame.
        text="Log In",  # Sets the button text.
        font=("Arial", 11, "bold"),  # Makes the button text bold.
        bg="#202020",  # Gives the button a dark-grey background.
        fg="white",  # Makes the button text white.
        activebackground="white",  # Makes the button white while clicked.
        activeforeground="black",  # Makes the text black while clicked.
        relief="flat",  # Removes the raised button border.
        bd=0,  # Removes the standard border.
        highlightthickness=2,  # Sets the thickness of the highlight border.
        highlightbackground="white",  # Makes the highlight border white.
        highlightcolor="white",  # Keeps the highlight border white when selected.
        cursor="hand2",  # Changes the mouse pointer over the button.
        command=login  # Calls the login function when clicked.
    )

    submit_button.pack(pady=10)  # Displays the login button.


# ==========================================================
# LOGIN FUNCTION
# ==========================================================

def login():  # Defines the function that checks the user's login details.
    global logged_in  # Allows this function to change the login status.
    global current_user  # Allows this function to store the current username.

    username = username_entry.get().strip()  # Gets the username and removes unwanted spaces.
    password = password_entry.get()  # Gets the password entered by the user.

    if not username or not password:  # Checks whether either input box is empty.
        message_label.config(  # Updates the login message.
            text="Please enter a username and password.",  # Explains that both fields are required.
            fg="red"  # Makes the error message red.
        )

        return  # Stops the login attempt.

    conn = sqlite3.connect("khaos.db")  # Opens the user database.
    cursor = conn.cursor()  # Creates a cursor for running SQL commands.

    cursor.execute(  # Searches the database for matching login details.
        "SELECT * FROM users WHERE username=? AND password=?",  # Uses placeholders to search safely.
        (username, password)  # Supplies the username and password to the placeholders.
    )

    result = cursor.fetchone()  # Gets the first matching user from the database.
    conn.close()  # Closes the database connection.

    if result:  # Checks whether a matching account was found.
        logged_in = True  # Changes the login status to logged in.
        current_user = username  # Stores the logged-in user's username.
        show_logged_in_navigation()  # Displays the navigation buttons for logged-in users.
        show_main_menu()  # Returns the user to the main menu.

    else:  # Runs when the username and password do not match an account.
        message_label.config(  # Updates the login message.
            text="Invalid username or password.",  # Explains that the login details were incorrect.
            fg="red"  # Makes the error message red.
        )


# ==========================================================
# REGISTER FUNCTION
# ==========================================================

def register():  # Defines the function that creates a new user account.
    username = register_username_entry.get().strip()  # Gets the new username and removes unwanted spaces.
    password = register_password_entry.get()  # Gets the new password.

    if not username or not password:  # Checks whether either registration field is empty.
        register_message_label.config(  # Updates the registration message.
            text="Please enter a username and password.",  # Explains that both fields are required.
            fg="red"  # Makes the error message red.
        )

        return  # Stops the registration attempt.

    conn = sqlite3.connect("khaos.db")  # Opens the user database.
    cursor = conn.cursor()  # Creates a cursor for running SQL commands.

    try:  # Attempts to add the new account to the database.
        cursor.execute(  # Runs the SQL command that creates the account.
            "INSERT INTO users (username, password) VALUES (?, ?)",  # Uses placeholders for the account details.
            (username, password)  # Supplies the username and password.
        )

        conn.commit()  # Saves the new account to the database.

        register_message_label.config(  # Updates the registration message.
            text="Registration successful!",  # Confirms that the account was created.
            fg="green"  # Makes the success message green.
        )

        register_username_entry.delete(0, tk.END)  # Clears the username input box.
        register_password_entry.delete(0, tk.END)  # Clears the password input box.

    except sqlite3.IntegrityError:  # Runs if the username already exists.
        register_message_label.config(  # Updates the registration message.
            text="Username already exists.",  # Explains why the account could not be created.
            fg="red"  # Makes the error message red.
        )

    finally:  # Runs whether registration succeeds or fails.
        conn.close()  # Closes the database connection.


# ==========================================================
# REGISTER PAGE
# ==========================================================

def show_register():  # Defines the function that displays the registration page.
    clear_content()  # Removes the content from the previous page.
    subtitle_label.config(text="Register")  # Changes the header subtitle.

    register_frame = tk.Frame(content_frame, bg="black")  # Creates a frame for the registration form.
    register_frame.pack(fill="both", expand=True)  # Makes the frame fill the content area.

    register_label = tk.Label(  # Creates the registration heading.
        register_frame,  # Places the heading inside the registration frame.
        text="Create an Account",  # Sets the heading text.
        font=("Arial", 18, "bold"),  # Makes the heading large and bold.
        bg="black",  # Gives the heading a black background.
        fg="white"  # Makes the heading text white.
    )

    register_label.pack(pady=(20, 15))  # Displays the heading.

    register_username_label = tk.Label(  # Creates the new username label.
        register_frame,  # Places the label inside the registration frame.
        text="Username:",  # Sets the label text.
        font=("Arial", 12),  # Sets the label font.
        bg="black",  # Gives the label a black background.
        fg="white"  # Makes the label text white.
    )

    register_username_label.pack(pady=5)  # Displays the username label.

    global register_username_entry  # Allows the register function to access this entry.

    register_username_entry = tk.Entry(  # Creates the new username input box.
        register_frame,  # Places the input box inside the registration frame.
        font=("Arial", 12),  # Sets the text font.
        width=25  # Sets the width of the input box.
    )

    register_username_entry.pack(pady=5)  # Displays the username input box.

    register_password_label = tk.Label(  # Creates the new password label.
        register_frame,  # Places the label inside the registration frame.
        text="Password:",  # Sets the label text.
        font=("Arial", 12),  # Sets the label font.
        bg="black",  # Gives the label a black background.
        fg="white"  # Makes the label text white.
    )

    register_password_label.pack(pady=(10, 5))  # Displays the password label.

    global register_password_entry  # Allows the register function to access this entry.

    register_password_entry = tk.Entry(  # Creates the new password input box.
        register_frame,  # Places the input box inside the registration frame.
        font=("Arial", 12),  # Sets the text font.
        width=25,  # Sets the width of the input box.
        show="*"  # Replaces the typed password with asterisks.
    )

    register_password_entry.pack(pady=5)  # Displays the password input box.

    global register_message_label  # Allows the register function to update this message.

    register_message_label = tk.Label(  # Creates the registration message label.
        register_frame,  # Places the message inside the registration frame.
        text="",  # Starts with no message.
        font=("Arial", 11),  # Sets the message font.
        bg="black",  # Gives the message a black background.
        fg="white"  # Makes the starting text white.
    )

    register_message_label.pack(pady=10)  # Displays the message area.

    register_button = tk.Button(  # Creates the Register button.
        register_frame,  # Places the button inside the registration frame.
        text="Register",  # Sets the button text.
        font=("Arial", 11, "bold"),  # Makes the button text bold.
        bg="#202020",  # Gives the button a dark-grey background.
        fg="white",  # Makes the button text white.
        activebackground="white",  # Makes the button white while clicked.
        activeforeground="black",  # Makes its text black while clicked.
        relief="flat",  # Removes the raised button border.
        bd=0,  # Removes the standard border.
        highlightthickness=2,  # Sets the thickness of the highlight border.
        highlightbackground="white",  # Makes the highlight border white.
        highlightcolor="white",  # Keeps the highlight border white when selected.
        cursor="hand2",  # Changes the mouse pointer over the button.
        command=register  # Calls the register function when clicked.
    )

    register_button.pack(pady=10)  # Displays the Register button.

    back_to_login_button = tk.Button(  # Creates the Back to Log In button.
        register_frame,  # Places the button inside the registration frame.
        text="Back to Log In",  # Sets the button text.
        font=("Arial", 11, "bold"),  # Makes the button text bold.
        bg="#202020",  # Gives the button a dark-grey background.
        fg="white",  # Makes the button text white.
        activebackground="white",  # Makes the button white while clicked.
        activeforeground="black",  # Makes its text black while clicked.
        relief="flat",  # Removes the raised button border.
        bd=0,  # Removes the standard border.
        cursor="hand2",  # Changes the mouse pointer over the button.
        command=show_login  # Returns to the login page when clicked.
    )

    back_to_login_button.pack(pady=5)  # Displays the Back to Log In button.


# ==========================================================
# LOGGED-OUT NAVIGATION
# ==========================================================

def show_logged_out_navigation():  # Defines the navigation shown to logged-out users.
    for widget in navigation_frame.winfo_children():  # Loops through the current navigation buttons.
        widget.destroy()  # Deletes each existing navigation button.

    main_menu_button = tk.Button(  # Creates the Main Menu button.
        navigation_frame,  # Places the button inside the navigation frame.
        text="Main Menu",  # Sets the button text.
        font=("Arial", 11, "bold"),  # Makes the button text bold.
        bg="#202020",  # Gives the button a dark-grey background.
        fg="white",  # Makes the button text white.
        activebackground="white",  # Makes the button white while clicked.
        activeforeground="black",  # Makes its text black while clicked.
        relief="flat",  # Removes the raised button border.
        bd=0,  # Removes the standard border.
        highlightthickness=2,  # Sets the highlight border thickness.
        highlightbackground="white",  # Makes the highlight border white.
        highlightcolor="white",  # Keeps the highlight border white when selected.
        cursor="hand2",  # Changes the mouse pointer over the button.
        command=show_main_menu  # Opens the main menu when clicked.
    )

    main_menu_button.pack(  # Displays the Main Menu button.
        side="left",  # Positions the button on the left.
        fill="both",  # Makes the button fill its allocated space.
        expand=True,  # Allows the button to expand.
        padx=5,  # Adds horizontal space around the button.
        pady=5,  # Adds vertical space around the button.
        ipady=12  # Adds space inside the button.
    )

    login_button = tk.Button(  # Creates the Log In/Sign Up button.
        navigation_frame,  # Places the button inside the navigation frame.
        text="Log In /\nSign Up",  # Displays the button text on two lines.
        font=("Arial", 11, "bold"),  # Makes the button text bold.
        bg="#202020",  # Gives the button a dark-grey background.
        fg="white",  # Makes the button text white.
        activebackground="white",  # Makes the button white while clicked.
        activeforeground="black",  # Makes its text black while clicked.
        relief="flat",  # Removes the raised button border.
        bd=0,  # Removes the standard border.
        highlightthickness=2,  # Sets the highlight border thickness.
        highlightbackground="white",  # Makes the highlight border white.
        highlightcolor="white",  # Keeps the highlight border white when selected.
        cursor="hand2",  # Changes the mouse pointer over the button.
        command=show_login  # Opens the login page when clicked.
    )

    login_button.pack(  # Displays the Log In/Sign Up button.
        side="left",  # Positions the button beside the Main Menu button.
        fill="both",  # Makes the button fill its allocated space.
        expand=True,  # Allows the button to expand.
        padx=5,  # Adds horizontal space around the button.
        pady=5,  # Adds vertical space around the button.
        ipady=12  # Adds space inside the button.
    )

# ==========================================================
# LOGGED-IN NAVIGATION
# ==========================================================

def show_logged_in_navigation():  # Defines the navigation shown to logged-in users.
    for widget in navigation_frame.winfo_children():  # Loops through the current navigation buttons.
        widget.destroy()  # Deletes each existing navigation button.

    main_menu_button = tk.Button(  # Creates the Main Menu button.
        navigation_frame,  # Places the button inside the navigation frame.
        text="Main Menu",  # Sets the button text.
        font=("Arial", 10, "bold"),  # Makes the button text bold.
        bg="#202020",  # Gives the button a dark-grey background.
        fg="white",  # Makes the button text white.
        activebackground="white",  # Makes the button white while clicked.
        activeforeground="black",  # Makes its text black while clicked.
        relief="flat",  # Removes the raised button border.
        bd=0,  # Removes the standard border.
        highlightthickness=2,  # Sets the highlight border thickness.
        highlightbackground="white",  # Makes the highlight border white.
        highlightcolor="white",  # Keeps the highlight border white when selected.
        cursor="hand2",  # Changes the mouse pointer over the button.
        command=show_main_menu  # Opens the main menu when clicked.
    )

    main_menu_button.pack(  # Displays the Main Menu button.
        side="left",  # Positions the button on the left.
        fill="both",  # Makes the button fill its allocated space.
        expand=True,  # Allows the button to expand.
        padx=3,  # Adds horizontal space around the button.
        pady=5,  # Adds vertical space around the button.
        ipady=10  # Adds space inside the button.
    )

    my_workout_button = tk.Button(  # Creates the My Workout button.
        navigation_frame,  # Places the button inside the navigation frame.
        text="My Workout",  # Sets the button text.
        font=("Arial", 10, "bold"),  # Makes the button text bold.
        bg="#202020",  # Gives the button a dark-grey background.
        fg="white",  # Makes the button text white.
        activebackground="white",  # Makes the button white while clicked.
        activeforeground="black",  # Makes its text black while clicked.
        relief="flat",  # Removes the raised button border.
        bd=0,  # Removes the standard border.
        highlightthickness=2,  # Sets the highlight border thickness.
        highlightbackground="white",  # Makes the highlight border white.
        highlightcolor="white",  # Keeps the highlight border white when selected.
        cursor="hand2",  # Changes the mouse pointer over the button.
        command=show_my_workout  # Opens the My Workout page when clicked.
    )

    my_workout_button.pack(  # Displays the My Workout button.
        side="left",  # Positions the button beside the previous button.
        fill="both",  # Makes the button fill its allocated space.
        expand=True,  # Allows the button to expand.
        padx=3,  # Adds horizontal space around the button.
        pady=5,  # Adds vertical space around the button.
        ipady=10  # Adds space inside the button.
    )

    exercise_library_button = tk.Button(  # Creates the Exercise Library button.
        navigation_frame,  # Places the button inside the navigation frame.
        text="Exercise\nLibrary",  # Displays the button text on two lines.
        font=("Arial", 10, "bold"),  # Makes the button text bold.
        bg="#202020",  # Gives the button a dark-grey background.
        fg="white",  # Makes the button text white.
        activebackground="white",  # Makes the button white while clicked.
        activeforeground="black",  # Makes its text black while clicked.
        relief="flat",  # Removes the raised button border.
        bd=0,  # Removes the standard border.
        highlightthickness=2,  # Sets the highlight border thickness.
        highlightbackground="white",  # Makes the highlight border white.
        highlightcolor="white",  # Keeps the highlight border white when selected.
        cursor="hand2",  # Changes the mouse pointer over the button.
        command=show_exercise_library  # Opens the Exercise Library when clicked.
    )

    exercise_library_button.pack(  # Displays the Exercise Library button.
        side="left",  # Positions the button beside the previous button.
        fill="both",  # Makes the button fill its allocated space.
        expand=True,  # Allows the button to expand.
        padx=3,  # Adds horizontal space around the button.
        pady=5,  # Adds vertical space around the button.
        ipady=10  # Adds space inside the button.
    )

    logout_button = tk.Button(  # Creates the Log Out button.
        navigation_frame,  # Places the button inside the navigation frame.
        text="Log Out",  # Sets the button text.
        font=("Arial", 10, "bold"),  # Makes the button text bold.
        bg="#202020",  # Gives the button a dark-grey background.
        fg="white",  # Makes the button text white.
        activebackground="white",  # Makes the button white while clicked.
        activeforeground="black",  # Makes its text black while clicked.
        relief="flat",  # Removes the raised button border.
        bd=0,  # Removes the standard border.
        highlightthickness=2,  # Sets the highlight border thickness.
        highlightbackground="white",  # Makes the highlight border white.
        highlightcolor="white",  # Keeps the highlight border white when selected.
        cursor="hand2",  # Changes the mouse pointer over the button.
        command=logout  # Calls the logout function when clicked.
    )

    logout_button.pack(  # Displays the Log Out button.
        side="left",  # Positions the button beside the previous button.
        fill="both",  # Makes the button fill its allocated space.
        expand=True,  # Allows the button to expand.
        padx=3,  # Adds horizontal space around the button.
        pady=5,  # Adds vertical space around the button.
        ipady=10  # Adds space inside the button.
    )

# ==========================================================
# DIVIDER
# ==========================================================

divider = tk.Frame(root, bg="white", height=5)  # Creates a white divider above the navigation bar.
divider.pack(fill="x", padx=8, pady=(0, 8))  # Displays the divider across the window.

# ==========================================================
# LOG OUT
# ==========================================================

def logout():  # Defines the function that logs the user out.
    global logged_in  # Allows the function to change the login status.
    global current_user  # Allows the function to clear the current username.

    logged_in = False  # Changes the login status to logged out.
    current_user = None  # Removes the stored username.
    show_logged_out_navigation()  # Displays the logged-out navigation buttons.
    show_main_menu()  # Returns the user to the main menu.


# ==========================================================
# START PROGRAM
# ==========================================================

show_logged_out_navigation()  # Starts the application with the logged-out navigation.
show_main_menu()  # Displays the main menu when the application starts.


# ==========================================================
# RUN PROGRAM
# ==========================================================

root.mainloop()  # Keeps the application open and waits for the user to interact with it.
