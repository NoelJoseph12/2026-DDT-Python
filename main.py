import tkinter as tk #Imports the tkinter library, which creates GUI's in Python. Also shortens it to 'tk'.
from PIL import Image, ImageTk #Imports the tools required to open and display images in the GUI.
from pathlib import Path #Imports the path to help find the image file in the same directory as the main.py file. (Used help from the teacher and websits to import and implement this into my code.)
import sqlite3 #Imports the sqlite3 library, which allows me to create and manage a database for the login system.



# DATABASE # 

def create_database(): #Defines a function called create_database() that creates a database called 'khaos.db' and a table called 'users' with two columns: 'username' and 'password'.
    conn = sqlite3.connect('khaos.db') #Opens the database file 'khaos.db'. If the file does not exist, it will be create it.
    cursor = conn.cursor() #Creates a cursor which allows me to execute SQL commands on the database.

    cursor.execute( #Runs an SQL command that creates a table called 'users' with two columns: 'username' and 'password'.
        "CREATE TABLE IF NOT EXISTS users (" #Creates a table called 'users' if it doesn't already exist.
           "username TEXT PRIMARY KEY," #Creates a unique 'username' column is the primary key, which means that it must be unique for each user. 
              "password TEXT NOT NULL)" #The 'password' column is not null, which means that it cannot be empty.
                   )

    #cursor.execute( # Runs an SQL command to add example accounts for testing.
        #"INSERT OR IGNORE INTO users (username, password) VALUES " # Adds users unless they already exist.
        #"('user1', 'pass123'), " # Adds the first example account.
        #"('user2', 'pass456'), " # Adds the second example account.
        #"('user3', 'pass789')" # Adds the third example account.
    #)

#Lines 18 to 23 are commented out because they were used for testing purposes and are no longer needed. The example accounts have been added to the database and do not need to be added again.

    conn.commit() #Saves the changes made to the database.
    conn.close() #Closes the connection to the database.

create_database() #Calls the function when the program starts.



# MAIN WINDOW #

root = tk.Tk() #Creates the main window of the application using the Tk() class from the tkinter library. This window will contain all my functions and other elements of my code.

#root.geometry("500x600") #Sets the size of the main window to 500 pixels wide and 600 pixels tall.
#root.geometry("zoomed") #Sets the size of the main window to be maximized to fill the entire screen. This is the wrong way to change the size of the main window.

root.state("zoomed") #Sets the size of the main window to be maximized to fill the entire screen. I used a youtube video to fix this issue.
root.title("Khaos - Workout Tracker") #Sets the title shown at the top of the main window to "Khaos - Workout Tracker".
root.configure(bg="black") #Changes the main window's background color to black. This is done to match the color scheme of the application and make it look more visually appealing and to fit my app's theme.



# LOGIN STATUS #

logged_in = False #Keeps track of whether a user is logged in or not. Initially set to False, indicating that no user is logged in when the application starts.
current_user = None #Stores the username of the currently logged-in user. Initially set to None, indicating that no user is logged in when the application starts.
my_workout_exercises = [] #Creates an empty list that will store all the exercises the user adds for their personal workout.


# EXERCISE DATA #

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
#To get all the data for such exercises I used another gym app called 'Hevy'.



# HEADER #

header_frame = tk.Frame(root, bg="black", height=250) #Creates a frame called header_frame that will contain the logo and title of the application. Helps with the organisation of my app's layout. The background color of the frame is set to black and the height is set to 250 pixels.
header_frame.pack(fill="x", padx=5, pady=5) #Places the header_frame at the top of the main window and fills the entire width of the window. The padx and pady parameters add padding around the frame to create some space between the frame and other elements in the window.
header_frame.pack_propagate(False) #Prevents the header_frame from resizing itself to fit its contents. This is done to ensure that the frame maintains its specified height of 250 pixels, regardless of the size of the logo and title within it.

image_path = Path(__file__).parent / "Khaos_Logo.png" #Finds the path to the image file "Khaos_Logo.png" in the same directory as the main.py file. This is done using the Path class from the pathlib library. Used help from the teacher and youtube videoes to help me understand how to use the Path class and implement it into my code.

try: #Tries to open the image file "Khaos_Logo.png" and display it in the header_frame.
    img = Image.open(image_path) #Opens the image file "Khaos_Logo.png" using the Image class from the PIL library. 
    img = img.resize((220, 220)) #Resizes the image to 220 pixels wide and 220 pixels tall.
    logo = ImageTk.PhotoImage(img) #Converts the image to a format that can be displayed in the tkinter GUI using the ImageTk class from the PIL library.

    logo_label = tk.Label( #Creates a label called logo_label that will help me display the logo image in the header_frame. The label is created using the Label class from the tkinter library.
        header_frame, #The header_frame is put inside the header.
        image=logo, #Displays the converted logo image in the label.
        bg="black" #Sets the background color of the label to black.
    )

    logo_label.pack(side="left", anchor="n") #Positions the logo_label and everything it contains to the upper left corner of the header_frame. Used help from videos and websites to understand positioning.

except FileNotFoundError: #Runs if the image file "Khaos_Logo.png" cannot be found in the same directory as the main.py file. This is done to handle the error and display a message to the user instead of crashing the application.
    error_label = tk.Label(header_frame, #Creates a label called error_label that will display and error message in the header_frame.
    text="Khaos_Logo.png could not be found.", #The error message that will be displayed in the label if the image file cannot be found.
    font=("Arial", 18), #The font of the error message is set to Arial with a size of 18.
    bg="black", #Makes the background color of the label black to match the header_frame.
    fg="red") #Sets the text color of the label to red.

    error_label.pack( #Makes the error_label to be displayed in the header_frame. The label is positioned to the left side of the frame and anchored to the top of the frame. I learnt about anchor from websites.
    side="left", #Makes the error_label to be displayed on the left side of the header_frame.
    anchor="n" #Anchors the error_label to the top of the header_frame. 
    )



# TITLE AND SUBTITLE #

text_frame = tk.Frame(header_frame, bg="black") #Creates a frame called text_frame that will contain the title and subtitle of the application. Helps with the organisation of my app's layout. The background color of the frame is set to black.
text_frame.place(relx=0.5, rely=0.5, anchor="center") #Positions the text_frame in the center of the header_frame. The relx and rely parameters set the position of the frame relative to the size of the header_frame. The anchor parameter sets the anchor point of the frame to the center.

title_label = tk.Label(text_frame, text="Khaos", font=("Arial", 40, "bold"), bg="black", fg="white") #Creates a label called title_label that will display the title of the application. The font is set to Arial with a size of 40 and bold style. The background color is set to black and the text color is set to white.
title_label.pack(pady=(0, 10)) #Packs the title_label into the text_frame with a padding of 10 pixels at the bottom.

subtitle_label = tk.Label(text_frame, text="Measure The Mayhem", font=("Arial", 25, "bold"), bg="black", fg="white") #Creates a label called subtitle_label that will display the subtitle of the application. The font is set to Arial with a size of 25 and bold style. The background color is set to black and the text color is set to white.
subtitle_label.pack() #Allows the subtitle_label to be displayed in the text_frame below the title_label.



# DIVIDER #

divider = tk.Frame(root, bg="white", height=5) #Creates a white divider that's 5 pixels tall.
divider.pack(fill="x", padx=8, pady=(0, 8)) #Displays the divider across the window.



# NAVIGATION FRAME #

navigation_frame = tk.Frame(root, bg="black", height=60) #Creates a frame called navigation_frame that will contain the navigation bar.
navigation_frame.pack(fill="x", padx=5, pady=5) #Places the navigation bar across the window using the fill function and also adds padding to help with positioning.


# CONTENT AREA #

content_frame = tk.Frame(root, bg="black") #Creates a frame called content_frame that will contain the main content of the application. Helps with the organisation of my app's layout. The background color of the frame is set to black.
content_frame.pack(fill="both", expand=True, padx=5, pady=5) #Fills the entire available space in the main window and expands to fill any additional space. The padx and pady parameters add padding around the frame to create some space between the frame and other elements in the window.



# CLEAR CONTENT AREA #
def clear_content(): #Defines a function called clear_content that removes the current page.
    for widget in content_frame.winfo_children(): #Loops through all the elements that are currently displayed in the content_frame. 
        widget.destroy() #Deletes each element in the content_frame, effectively clearing the content area before loading a new page. 

#For lines 103 to 113, I used help from a youtube video as when this wasn't in my code it kept breaking when I tried to change pages. I learnt that this function is used to clear the content area before loading a new page, preventing overlapping content and ensuring that only the relevant page is displayed at any given time.



# MAIN MENU #

def show_main_menu(): #Defines the function show_main_menu that displays the main menu.
    clear_content() #Removes the content from the previous page.

    subtitle_label.config(text="Measure The Mayhem") #Changes the subtitle back to the set text.

    title = tk.Label( #Creates the main menu heading.
        content_frame, #Places the heading inside the content area.
        text="Welcome to Khaos", #Sets the heading text to "Welcome to Khaos".
        font=("Arial", 22, "bold"), #Makes the heading text font arial, size 22 and bold.
        bg="black", #Gives the heading a black background.
        fg="white" #Makes the heading text white.
    )

    title.pack(pady=(25, 10)) #Displays the heading with padding around it.

    message = tk.Label( #Creates an instruction message.
        content_frame, #Places the message inside the content area.
        text="Choose An Option From The Navigation Bar", #Tells the user what to do.
        font=("Arial", 12), #Sets the text font to arial and the text size to 12.
        bg="black", #Gives the text a black background.
        fg="white" #Makes the text white.
    )

    message.pack(pady=5) #Displays the instruction message.



# MY WORKOUT # 

def show_my_workout(): #Defines the function 'show_my_workout' which displays the My Workout page.
    if not logged_in: #Checks whether the user is logged in.
        show_login() #Sends logged out users to the login page.
        return #Stops the rest of this function from running.

    clear_content() #Removes the content from the previous page.
    subtitle_label.config(text="My Workout")

    title = tk.Label( #Creates the 'My Workout' heading.
        content_frame, #Places the heading inside the content area.
        text="My Workout", #Sets the heading text.
        font=("Arial", 22, "bold"), #Makes the heading font arial, size 22 and bold.
        bg="black", #Gives the heading text a black background.
        fg="white" #Makes the heading text white.
    )

    title.pack(pady=(25, 15)) #Displays the heading with padding around it.

    if not my_workout_exercises: #Checks whether the user has no saved exercises.
        message = tk.Label( #Creates a text for the My Workout page.
            content_frame, #Places the text inside the content area.
            text="Your Selected Workouts Will Appear Here", #Displays the set text, informing the user that their selected workouts would appear there.
            font=("Arial", 12), #Sets the text font to arial and size 12.
            bg="black", #Gives the text a black background.
            fg="white" #Makes the text white.
        )

        message.pack(pady=5) #Displays the message with 5 pixels of padding around it.
        return #Stops the function because there are no exercises to display.

    list_frame = tk.Frame( #Creates a frame to hold the user's saved exercises.
        content_frame, #Places the exercise list inside the content area.
        bg="black" #Gives the exercise list a black background.
    )

    list_frame.pack( #Displays the frame containing the exercise list.
        fill="both", #Makes the frame fill the available width and height.
        expand=True, #Allows the frame to grow when the window gets larger.
        padx=20 #Adds 20 pixels of padding to the left and right.
    )

    def remove_exercise(exercise): #Defines the function remove_exercise allowing users to remove a previously selected exercise.
        my_workout_exercises.remove(exercise) #Removes the selected exercise from the list.
        show_my_workout() #Reloads the page to show the updated exercise list.

    for exercise in my_workout_exercises: #Loops through every saved exercise.
        row = tk.Frame( #Creates a separate row for the current exercise.
            list_frame, #Places the row inside the exercise list.
            bg="#202020" #Gives the row a grey background.
        )

        row.pack( #Displays the exercise row.
            fill="x", #Makes the row fill the available width.
            pady=6 #Adds six pixels of space above and below the row.
        )

        info = tk.Frame( #Creates a frame for the exercise information.
            row, #Places the information inside the exercise row.
            bg="#202020" #Gives it the same background colour as the row.
        )

        info.pack( #Displays the exercise-information frame.
            side="left", #Places the information on the left side of the row.
            fill="x", #Makes the information fill the available width.
            expand=True, #Allows the information area to use the extra space.
            padx=12, #Adds space to the left and right.
            pady=10 #Adds space above and below.
        )

        tk.Label( #Creates a label displaying the exercise's name.
            info, #Places the label inside the information frame.
            text=exercise["name"], #Gets the exercise name from its dictionary.
            font=("Arial", 12, "bold"), #Makes the exercise name bold.
            bg="#202020", #Gives the label a dark grey background.
            fg="white", #Makes the exercise name white.
            anchor="w" #Positions the text on the left side of the label.
        ).pack(fill="x") #Displays the label across the available width.

        tk.Label( #Creates a label displaying the exercise's category.
            info, #Places the label inside the information frame.
            text=exercise["category"], #Gets the category from the exercise dictionary.
            font=("Arial", 10), #Sets the category's font to arial and size 10.
            bg="#202020", #Gives the label a grey background.
            fg="#a9a9a9", #Makes the category text light grey.
            anchor="w" #Positions the text on the left side of the label.
        ).pack(fill="x") #Displays the label across the available width.

        tk.Button( #Creates a button that removes the exercise.
            row, #Places the button inside the exercise row.
            text="Remove", #Sets the text displayed on the button.
            font=("Arial", 10, "bold"), #Makes the button text font arial, size 10 and bold.
            bg="#202020", #Gives the button a grey background.
            fg="white", #Makes the button text white.
            activebackground="white", #Changes the button background to white while it is being clicked.
            activeforeground="black", #Changes the button text to black while it is being clicked.
            relief="flat", #Makes the button appear flat instead of raised.
            bd=0, #Removes the standard border around the button.
            cursor="hand2", #Changes the mouse cursor into a hand when it is over the button.

            #I learnt the below line through websites and videos as it was very confusing to implement into my code. Saves the current exercise as "ex" and removes that exercise when the button is clicked.
            command=lambda ex=exercise: remove_exercise(ex)).pack( #Displays and positions the 'Remove' button inside the exercise row. 
            #This line tells the button to remove the correct exercise when clicked. The lambda waits for the click, ex=exercise remembers which exercise belongs to the button, and remove_exercise(ex) removes it. The .pack() part then displays and positions the button.
            side="right", #Positions the button on the right side of the row.
            padx=12, #Adds 12 pixels of space outside the left and right sides of the button.
            ipady=4 #Adds four pixels of space inside the button to make it taller.
        )



# EXERCISE LIBRARY

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

def register():
    username = register_username_entry.get().strip()
    password = register_password_entry.get()

    if not username or not password:
        register_message_label.config(
            text="Please enter a username and password.",
            fg="red"
        )
        return

    conn = sqlite3.connect("khaos.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()

        register_message_label.config(
            text="Registration successful!",
            fg="green"
        )

        register_username_entry.delete(0, tk.END)
        register_password_entry.delete(0, tk.END)

    except sqlite3.IntegrityError:
        register_message_label.config(
            text="Username already exists.",
            fg="red"
        )

    finally:
        conn.close()


# ==========================================================
# REGISTER PAGE
# ==========================================================

def show_register():
    clear_content()
    subtitle_label.config(text="Register")

    register_frame = tk.Frame(content_frame, bg="black")
    register_frame.pack(fill="both", expand=True)

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

    register_username_label.pack(pady=5)

    global register_username_entry

    register_username_entry = tk.Entry(
        register_frame,
        font=("Arial", 12),
        width=25
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

    global register_password_entry

    register_password_entry = tk.Entry(
        register_frame,
        font=("Arial", 12),
        width=25,
        show="*"
    )

    register_password_entry.pack(pady=5)

    global register_message_label

    register_message_label = tk.Label(
        register_frame,
        text="",
        font=("Arial", 11),
        bg="black",
        fg="white"
    )

    register_message_label.pack(pady=10)

    register_button = tk.Button(
        register_frame,
        text="Register",
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
        command=register
    )

    register_button.pack(pady=10)

    back_to_login_button = tk.Button(
        register_frame,
        text="Back to Log In",
        font=("Arial", 11, "bold"),
        bg="#202020",
        fg="white",
        activebackground="white",
        activeforeground="black",
        relief="flat",
        bd=0,
        cursor="hand2",
        command=show_login
    )

    back_to_login_button.pack(pady=5)


# ==========================================================
# LOGGED-OUT NAVIGATION
# ==========================================================

def show_logged_out_navigation():
    for widget in navigation_frame.winfo_children():
        widget.destroy()

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
        command=show_main_menu
    )

    main_menu_button.pack(
        side="left",
        fill="both",
        expand=True,
        padx=5,
        pady=5,
        ipady=12
    )

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
        command=show_login
    )

    login_button.pack(
        side="left",
        fill="both",
        expand=True,
        padx=5,
        pady=5,
        ipady=12
    )


# ==========================================================
# LOGGED-IN NAVIGATION
# ==========================================================

def show_logged_in_navigation():
    for widget in navigation_frame.winfo_children():
        widget.destroy()

    main_menu_button = tk.Button(
        navigation_frame,
        text="Main Menu",
        font=("Arial", 10, "bold"),
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
        command=show_main_menu
    )

    main_menu_button.pack(
        side="left",
        fill="both",
        expand=True,
        padx=3,
        pady=5,
        ipady=10
    )

    my_workout_button = tk.Button(
        navigation_frame,
        text="My Workout",
        font=("Arial", 10, "bold"),
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
        command=show_my_workout
    )

    my_workout_button.pack(
        side="left",
        fill="both",
        expand=True,
        padx=3,
        pady=5,
        ipady=10
    )

    exercise_library_button = tk.Button(
        navigation_frame,
        text="Exercise\nLibrary",
        font=("Arial", 10, "bold"),
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
        command=show_exercise_library
    )

    exercise_library_button.pack(
        side="left",
        fill="both",
        expand=True,
        padx=3,
        pady=5,
        ipady=10
    )

    logout_button = tk.Button(
        navigation_frame,
        text="Log Out",
        font=("Arial", 10, "bold"),
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
        command=logout
    )

    logout_button.pack(
        side="left",
        fill="both",
        expand=True,
        padx=3,
        pady=5,
        ipady=10
    )



# LOG OUT #

def logout(): 
    global logged_in
    global current_user 

    logged_in = False
    current_user = None 
    show_logged_out_navigation() 
    show_main_menu()



# DIVIDER #

divider = tk.Frame(root, bg="white", height=5) #Creates a white divider that's 5 pixels tall.
divider.pack(fill="x", padx=8, pady=(0, 8)) #Displays the divider across the window.



# START PROGRAM #

show_logged_out_navigation() #Starts the application with the logged out navigation.
show_main_menu() #Displays the main menu when the application starts.



# RUN CODE # 

root.mainloop() #Keeps the application open and waits for the user to interact with it.