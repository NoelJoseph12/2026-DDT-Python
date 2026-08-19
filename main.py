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
        text="Choose an option from the navigation bar.", #Tells the user what to do.
        font=("Arial", 12), #Sets the text font to arial and the text size to 12.
        bg="black", #Gives the text a black background.
        fg="white" #Makes the  text white.
    )

    message.pack(pady=5) #Displays the instruction message.



# RUN CODE # 

root.mainloop() #Keeps the application open and waits for the user to interact with it.