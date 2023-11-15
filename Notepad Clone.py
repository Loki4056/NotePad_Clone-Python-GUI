import os
import csv
import sqlite3
import tkinter as tk
import datetime
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import *
from tkinter.filedialog import *
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk

class Notepad:
    def __init__(self, master):
        self.root = master
        # Set the window text
        self.root.title("Untitled - Notepad")
        self.root.attributes('-fullscreen', True)

        self.logged_in = False
        self.username = ""
        self.password = ""

        self.Width = 600
        self.Height = 400

        self.TextArea = Text(self.root)
        self.TextArea.pack(fill=BOTH, expand=YES)

        self.MenuBar = Menu(self.root)
        self.FileMenu = Menu(self.MenuBar, tearoff=0)
        self.EditMenu = Menu(self.MenuBar, tearoff=0)
        self.HelpMenu = Menu(self.MenuBar, tearoff=0)
        self.ThemeMenu = Menu(self.MenuBar, tearoff=0)
        
        self.root.config(menu=self.MenuBar)

        self.ScrollBar = Scrollbar(self.TextArea)
        self.file = None

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.FileMenu.add_command(label="New", command=self.newFile, accelerator="Ctrl+N")
        self.FileMenu.add_command(label="Open", command=self.openFile, accelerator="Ctrl+O")
        self.FileMenu.add_command(label="Save", command=self.saveFile, accelerator="Ctrl+S")
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label="Exit", command=self.quitApplication)
        self.MenuBar.add_cascade(label="File", menu=self.FileMenu)

        self.EditMenu.add_command(label="Cut", command=self.cut)
        self.EditMenu.add_command(label="Copy", command=self.copy)
        self.EditMenu.add_command(label="Paste", command=self.paste)
        self.EditMenu.add_separator()
        self.EditMenu.add_command(label="Find", command=self.findText, accelerator="Ctrl+F")
        self.MenuBar.add_cascade(label="Edit", menu=self.EditMenu)

        self.ThemeMenu = Menu(self.MenuBar, tearoff=0)
        self.ThemeMenu.add_command(label="Toggle Theme", command=self.toggle_theme)
        self.MenuBar.add_cascade(label="Theme", menu=self.ThemeMenu)

        self.light_theme = ttk.Style()
        self.light_theme.theme_use("default")

        self.dark_theme = ttk.Style()
        self.dark_theme.theme_use("clam")

        self.theme_mode = "light"

        self.HelpMenu.add_command(label="About Notepad", command=self.showAbout)
        self.MenuBar.add_cascade(label="Help", menu=self.HelpMenu)

        self.TextArea.pack(fill=BOTH, expand=YES)

        self.ScrollBar = Scrollbar(self.TextArea)
        self.ScrollBar.pack(side=RIGHT, fill=Y)
        self.ScrollBar.config(command=self.TextArea.yview)
        self.TextArea.config(yscrollcommand=self.ScrollBar.set)

        self.root.bind('<Control-o>', self.openFile)  # Ctrl+O for Open
        self.root.bind('<Control-s>', self.saveFile)  # Ctrl+S for Save
        self.root.bind('<Control-n>', self.newFile)   # Ctrl+N for New
        self.root.bind('<Control-f>', self.findText)   # Ctrl+F for Find

    def toggle_theme(self):
        if self.theme_mode == "light":
            self.light_theme.configure("TText", background="black", foreground="white")
            self.TextArea.configure(bg="black", fg="white")
            self.root.tk.call("tk_setPalette", "white")
            self.theme_mode = "dark"
        else:
            self.light_theme.configure("TText", background="white", foreground="black")
            self.TextArea.configure(bg="white", fg="black")
            self.root.tk.call("tk_setPalette", "black")
            self.theme_mode = "light"

    def quitApplication(self):
        self.root.destroy()

    def showAbout(self):
        showinfo("Notepad", "Logeshkumar K")

    def openFile(self, event=None):
        self.file = askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.file == "":
            self.file = None
        else:
            self.root.title(os.path.basename(self.file) + " - Notepad")
            self.TextArea.delete(1.0, END)
            file = open(self.file, "r")
            self.TextArea.insert(1.0, file.read())
            file.close()

    def newFile(self, event=None):
        self.root.title("Untitled - Notepad")
        self.file = None
        self.TextArea.delete(1.0, END)

    def saveFile(self, event=None):
        if self.file is None:
            self.file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                                          filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
            if self.file == "":
                self.file = None
            else:
                file = open(self.file, "w")
                file.write(self.TextArea.get(1.0, END))
                file.close()
                self.root.title(os.path.basename(self.file) + " - Notepad")
        else:
            file = open(self.file, "w")
            file.write(self.TextArea.get(1.0, END))
            file.close()

    def cut(self):
        self.TextArea.event_generate("<<Cut>>")

    def copy(self):
        self.TextArea.event_generate("<<Copy>>")

    def paste(self):
        self.TextArea.event_generate("<<Paste>>")

    def findText(self, event=None):
        search_str = askstring("Find", "Enter text to find:")
        if search_str:
            content = self.TextArea.get(1.0, END)
            index = content.find(search_str)
            if index != -1:
                self.TextArea.tag_remove("highlight", 1.0, END)
                start_index = f"1.0 + {index} chars"
                end_index = f"{start_index} + {len(search_str)} chars"
                self.TextArea.tag_add("highlight", start_index, end_index)
                self.TextArea.tag_configure("highlight", background="yellow")
                self.TextArea.mark_set(INSERT, start_index)
                self.TextArea.see(INSERT)
            else:
                showinfo("Find", "Text not found")

    def run(self):
        self.root.mainloop()

class LoginFrame:
    background_photo_fullscreen = None  # Define background_photo_fullscreen as a class attribute

    def __init__(self, master):
        self.root = master 
        self.master = master
        self.admin_username = "admin"
        self.admin_password = "adminpass"
        self.master.title("Login")
        self.master.attributes('-fullscreen', True)
        self.edit_user_window = None  # Keep track of the edit user window
        self.view_all_users_window = None  # Keep track of the view all users window
        
        background_image_fullscreen = Image.open("Notepad Clone/1508669.jpg")
        resized_image_fullscreen = background_image_fullscreen.resize((self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        self.background_photo_fullscreen = ImageTk.PhotoImage(resized_image_fullscreen)

        # Create a label to display the blue carbon background image
        self.background_frame = tk.Label(master, image=self.background_photo_fullscreen)
        self.background_frame.place(x=0, y=0, relwidth=1, relheight=1)

        self.admin_frame = tk.Frame(master)
        self.admin_frame.pack()

        self.admin_ID_label = tk.Label(self.admin_frame, text="Admin ID:", font=("Arial", 14))
        self.admin_ID_label.pack(pady=10)

        self.admin_ID_entry = tk.Entry(self.admin_frame, width=50, font=("Arial", 12))
        self.admin_ID_entry.pack()

        self.admin_PW_label = tk.Label(self.admin_frame, text="Admin Password:", font=("Arial", 14))
        self.admin_PW_label.pack(pady=10)

        self.admin_PW_entry = tk.Entry(self.admin_frame, show="*", width=50, font=("Arial", 12))
        self.admin_PW_entry.pack()

        self.admin_login_button = tk.Button(self.admin_frame, text="Login as Admin", command=self.admin_login, font=("Arial", 12))
        self.admin_login_button.pack(pady=10)
        
        self.user_login_button = tk.Button(self.admin_frame, text="User Login", command=self.show_user_login, font=("Arial", 12))
        self.user_login_button.pack(pady=10)

        self.view_all_users_button = tk.Button(self.admin_frame, text="View All Users", command=self.view_all_users, font=("Arial", 12))
        self.view_all_users_button.pack(pady=10)

        self.admin_logout_button = tk.Button(self.admin_frame, text="logout as admin", command=self.logout_as_admin, font=("Arial", 12))
        self.admin_logout_button.pack(pady=10)

        self.login_frame = tk.Frame(self.master)  # Create a frame for login content
        self.login_frame.pack()

        self.username_label = tk.Label(self.login_frame, text="Username:", font=("Arial", 14))
        self.username_label.pack(pady=10)

        self.username_entry = tk.Entry(self.login_frame, width=50, font=("Arial", 12))
        self.username_entry.pack(pady=10, padx=10)

        self.password_label = tk.Label(self.login_frame, text="Password:", font=("Arial", 14))
        self.password_label.pack(pady=10)

        self.password_entry = tk.Entry(self.login_frame, show="*", width=50, font=("Arial", 12))
        self.password_entry.pack(pady=10, padx=10)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.user_login, font=("Arial", 12))
        self.login_button.pack(pady=10)
        
        self.admin_login_button1 = tk.Button(self.login_frame, text="Admin Login", command=self.show_admin_login, font=("Arial", 12))
        self.admin_login_button1.pack(pady=10)

        self.register_button = tk.Button(self.login_frame, text="Register", command=self.show_register_frame, font=("Arial", 12))
        self.register_button.pack(pady=10)
        
        self.register_frame = tk.Frame(self.master)
        self.register_frame.pack()

        self.register_first_name_label = tk.Label(self.register_frame, text="First Name:", font=("Arial", 14))
        self.register_first_name_label.pack(pady=10)

        self.register_first_name_entry = tk.Entry(self.register_frame, width=50, font=("Arial", 12))
        self.register_first_name_entry.pack(pady=10, padx=10)

        self.register_last_name_label = tk.Label(self.register_frame, text="Last Name:", font=("Arial", 14))
        self.register_last_name_label.pack(pady=10)

        self.register_last_name_entry = tk.Entry(self.register_frame, width=50, font=("Arial", 12))
        self.register_last_name_entry.pack(pady=10, padx=10)

        self.register_email_label = tk.Label(self.register_frame, text="Email Id:", font=("Arial", 14))
        self.register_email_label.pack(pady=10)

        self.register_email_entry = tk.Entry(self.register_frame, width=50, font=("Arial", 12))
        self.register_email_entry.pack(pady=10, padx=10)

        self.register_username_label = tk.Label(self.register_frame, text="Username:", font=("Arial", 14))
        self.register_username_label.pack(pady=10)

        self.register_username_entry = tk.Entry(self.register_frame, width=50, font=("Arial", 12))
        self.register_username_entry.pack(pady=10, padx=10)

        self.register_password_label = tk.Label(self.register_frame, text="Set Password:", font=("Arial", 14))
        self.register_password_label.pack(pady=10)

        self.register_password_entry = tk.Entry(self.register_frame, show="*", width=50, font=("Arial", 12))
        self.register_password_entry.pack(pady=10, padx=10)

        self.register_button = tk.Button(self.register_frame, text="Register", command=self.register_user, font=("Arial", 12))
        self.register_button.pack(pady=10)

        self.login_button = tk.Button(self.register_frame, text="User Login", command=self.show_login_frame, font=("Arial", 12))
        self.login_button.pack(pady=10)

        self.exit_button = tk.Button(self.register_frame, text="Quit", command=self.quit_login_screen, font=("Arial", 12))
        self.exit_button.pack(pady=10)

        self.exit_button = tk.Button(self.login_frame, text="Quit", command=self.quit_login_screen, font=("Arial", 12))
        self.exit_button.pack(pady=10)

        self.exit_button = tk.Button(self.admin_frame, text="Quit", command=self.quit_login_screen, font=("Arial", 12))
        self.exit_button.pack(pady=10)

        self.register_frame.pack_forget()  # Hide the register frame initially
        self.view_all_users_button.pack_forget()
        self.admin_logout_button.pack_forget()
        self.admin_frame.pack_forget()
        self.show_login_frame()
        
        self.csv_file_path = "user_logins.csv"  # CSV file for storing login and registration data

        self.db_connection = sqlite3.connect("user_details.db")
        self.create_table()  # Create the table if it doesn't exist    

    def admin_login(self):
        admin_username = self.admin_ID_entry.get()
        admin_password = self.admin_PW_entry.get()

        if admin_username == self.admin_username and admin_password == self.admin_password:
            # Correct admin credentials, grant access to admin controls
            self.admin_logged_in = True
            self.admin_ID_entry.config(state=tk.DISABLED)
            self.admin_PW_entry.config(state=tk.DISABLED)
            self.admin_login_button.config(state=tk.DISABLED)

            # Hide the admin login button
            self.admin_login_button.pack_forget()

            # Show the admin buttons
            self.view_all_users_button.pack()
            self.admin_logout_button.pack()

            messagebox.showinfo("Admin Login Successful", "You are logged in as Admin.")
        else:
            messagebox.showerror("Admin Login Failed", "Incorrect admin username or password.")

    def view_all_users(self):
        # Fetch all user information from the database
        query = "SELECT * FROM user_info"
        cursor = self.db_connection.cursor()
        cursor.execute(query)
        all_users = cursor.fetchall()
        cursor.close()
        
        if not all_users:
            # If there are no users, show a message
            messagebox.showinfo("View All Users", "No users found.")
        else:
            # Create a new window to display user details
            users_window = tk.Toplevel(self.master)
            users_window.title("All Users")

            # Create a canvas for scrolling
            canvas = tk.Canvas(users_window)
            canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

            # Create a scrollbar and associate it with the canvas
            scrollbar = tk.Scrollbar(users_window, command=canvas.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            canvas.config(yscrollcommand=scrollbar.set)

            # Create a frame to contain the user details
            users_frame = tk.Frame(users_window)
            users_frame.pack(padx=20, pady=20)

            # Header labels
            headers = ["User ID", "First Name", "Last Name", "Email", "Username", "Password"]
            for col, header in enumerate(headers):
                header_label = tk.Label(users_frame, text=header, font=("Arial", 12, "bold"))
                header_label.grid(row=0, column=col, padx=5, pady=5)

            # User data
            for row, user in enumerate(all_users, start=1):
                for col, data in enumerate(user):
                    user_label = tk.Label(users_frame, text=data, font=("Arial", 12))
                    user_label.grid(row=row, column=col, padx=5, pady=5)

                # Add Edit and Delete buttons for each user row
                edit_button = tk.Button(users_frame, text="Edit", command=lambda user_id=user[0]: self.edit_user_details(user_id))
                edit_button.grid(row=row, column=len(headers), padx=5, pady=5)

                delete_button = tk.Button(users_frame, text="Delete", command=lambda user=user: self.delete_user(user[0]))
                delete_button.grid(row=row, column=len(headers)+1, padx=5, pady=5)

            # Configure canvas scrolling region
            users_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

            # Bind canvas scrolling to mousewheel
            canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * (event.delta // 120), "units"))

            # Adjust the window size based on the number of users
            users_window.state('zoomed')  # Maximize the window to full screen    

    def edit_user_details(self, user_id):
        # Fetch user information from the database based on user_id
        query = "SELECT * FROM user_info WHERE User_ID = ?"
        cursor = self.db_connection.cursor()
        cursor.execute(query, (user_id,))
        user_info = cursor.fetchone()
        cursor.close()

        if user_info:
            self.show_edit_user_window(user_info)
        else:
            messagebox.showerror("Error", "User information not found.")

        if self.view_all_users is None:
                    self.show_edit_user_window()
        else:
                    self.show_edit_user_window.lift()

    def show_edit_user_window(self, user_info):
        user_id, first_name, last_name, email, username, password = user_info

        # Create a new window to edit user details
        edit_user_window = tk.Toplevel(self.master)
        edit_user_window.title("Edit User Details")

        # Create a frame to contain the user details form
        edit_user_frame = tk.Frame(edit_user_window)
        edit_user_frame.pack(padx=10, pady=10)

        # Editable fields
        first_name_label = tk.Label(edit_user_frame, text="First Name:", font=("Arial", 14))
        first_name_label.pack(anchor="w", padx=10, pady=10)
        first_name_entry = tk.Entry(edit_user_frame, font=("Arial", 12))
        first_name_entry.pack(fill="x", padx=10, pady=10)
        first_name_entry.insert(tk.END, first_name)

        last_name_label = tk.Label(edit_user_frame, text="Last Name:", font=("Arial", 14))
        last_name_label.pack(anchor="w", padx=10, pady=10)
        last_name_entry = tk.Entry(edit_user_frame, font=("Arial", 12))
        last_name_entry.pack(fill="x", padx=10, pady=10)
        last_name_entry.insert(tk.END, last_name)

        email_label = tk.Label(edit_user_frame, text="Email Id:", font=("Arial", 14))
        email_label.pack(anchor="w", padx=10, pady=10)
        email_entry = tk.Entry(edit_user_frame, font=("Arial", 12))
        email_entry.pack(fill="x", padx=10, pady=10)
        email_entry.insert(tk.END, email)

        # Disable editing of the username field
        username_label = tk.Label(edit_user_frame, text="Username:", font=("Arial", 14))
        username_label.pack(anchor="w", padx=10, pady=10)
        username_entry = tk.Entry(edit_user_frame, font=("Arial", 12))
        username_entry.pack(fill="x", padx=10, pady=10)
        username_entry.insert(tk.END, username)

        password_label = tk.Label(edit_user_frame, text="Set Password:", font=("Arial", 14))
        password_label.pack(anchor="w", padx=10, pady=10)
        password_entry = tk.Entry(edit_user_frame, font=("Arial", 12))
        password_entry.pack(fill="x", padx=10, pady=10)
        password_entry.insert(tk.END, password)

        # Label and Entry pairs for each attribute
        attribute_labels = ["First Name", "Last Name", "Email", "Username", "Set Password"]
        attribute_entries = [first_name, last_name, email, username, password]

        for label_text, entry_text in zip(attribute_labels, attribute_entries):
            label = tk.Label(edit_user_frame, text=f"{label_text}:", font=("Arial", 14))
            label.pack(anchor="w", padx=10, pady=10)
            entry = tk.Entry(edit_user_frame, font=("Arial", 12))
            entry.pack(fill="x", padx=10, pady=10)
            entry.insert(tk.END, entry_text)
            break
        # Save button to update the user details
        save_button = tk.Button(edit_user_frame, text="Save Changes", command=lambda: self.update_user(user_id, attribute_entries[0].get(), attribute_entries[1].get(), attribute_entries[2].get(), attribute_entries[4].get()))
        save_button.pack(side="right", padx=10, pady=10)

    def close_view_all_users_window(self):
        self.view_all_users_window.destroy()
        self.view_all_users_window = None
    
    def close_edit_user_window(self):
        self.edit_user_window.destroy()
        self.edit_user_window = None

    def update_user(self, user_id, first_name, last_name, email, username, password):
        query = "UPDATE user_info SET FirstName=?, LastName=?, Email=?, Username=?, Password=? WHERE User_ID=?"
        cursor = self.db_connection.cursor()
        cursor.execute(query, (first_name, last_name, email, username, password, user_id))
        self.db_connection.commit()
        cursor.close()
        messagebox.showinfo("Success", "User details updated successfully.")
        # Refresh the view_all_users window to reflect the updated details
        self.view_all_users()

    def delete_user(self, user_id):
        result = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this user?")
        if result:
            query = "DELETE FROM user_info WHERE User_ID=?"
            cursor = self.db_connection.cursor()
            cursor.execute(query, (user_id,))
            self.db_connection.commit()
            cursor.close()
            messagebox.showinfo("Success", "User deleted successfully.")
            # Refresh the view_all_users window to reflect the updated list
            self.view_all_users()

    def logout_as_admin(self):
        self.admin_logged_in = False
        self.admin_ID_entry.config(state=tk.NORMAL)  # Fix this line
        self.admin_PW_entry.config(state=tk.NORMAL)  # Fix this line
        self.admin_login_button.config(state=tk.NORMAL)

        self.view_all_users_button.pack_forget()
        self.admin_logout_button.pack_forget()
        self.admin_login_button.pack()

        # Optionally, clear admin login fields if needed
        self.admin_ID_entry.delete(0, tk.END)
        self.admin_PW_entry.delete(0, tk.END)

        messagebox.showinfo("Admin Logout", "You are logged out as Admin.")

    def show_admin_login(self):
        # Hide the login frame and show the admin login frame
        self.login_frame.pack_forget()
        self.admin_frame.pack()
        
        self.admin_ID_entry.delete(0, tk.END)
        self.admin_PW_entry.delete(0, tk.END)
        # Optionally, clear user login fields if needed
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END) 

    def show_user_login(self):
        # Hide the admin login frame and show the user login frame
        self.admin_frame.pack_forget()
        self.login_frame.pack()

        # Optionally, clear admin login fields if needed
        self.admin_ID_entry.delete(0, tk.END)
        self.admin_PW_entry.delete(0, tk.END)
        # Optionally, clear user login fields if needed
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def create_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username VARCHAR(255),
                password VARCHAR(255),
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                email VARCHAR(255)
            );
        """)
        self.db_connection.commit()

    def show_login_frame(self):
        self.register_frame.pack_forget()
        self.login_frame.pack()

    def show_register_frame(self):
        self.login_frame.pack_forget()
        self.register_frame.pack()

    def quit_login_screen(self):
            self.root.destroy()

    def show_notepad(self):
        self.master.withdraw()  # Hide the login window
        notepad_frame = tk.Toplevel(self.master)
        notepad_frame.attributes('-fullscreen', True)  # Set notepad frame to full screen
        notepad_app = Notepad(notepad_frame)
        notepad_app.run()

    def user_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT * FROM user_info WHERE username=? AND password=?", (username, password))
            user_data = cursor.fetchone()

            if user_data:
                self.show_notepad()  # Show the notepad widget
                self.master.withdraw()  # Hide the login frame
                messagebox.showinfo("Success Message!!!", "Login Successful!!!")
            else:
                messagebox.showerror("Attention!!!", "Incorrect username or password")
        else:
            messagebox.showwarning("Attention!!!", "Please enter both username and password.")

    def show_register_frame(self):
            self.login_frame.pack_forget()
            self.register_frame.pack()

    def register_user(self):
        first_name = self.register_first_name_entry.get()
        last_name = self.register_last_name_entry.get()
        email = self.register_email_entry.get()
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()

        if first_name and last_name and email and username and password:
            cursor = self.db_connection.cursor()
            try:
                cursor.execute("INSERT INTO user_info (username, password, first_name, last_name, email) VALUES (?, ?, ?, ?, ?)",
                               (username, password, first_name, last_name, email))
                self.db_connection.commit()
                messagebox.showinfo("Success!!!", "Registered new user successfully!!!")
                
                # Hide the register frame and show the login frame again
                self.register_frame.pack_forget()
                self.login_frame.pack()
                self.show_login_frame()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists. Please choose a different username.")
        else:
            messagebox.showwarning("Attention!!!", "Please fill in all the fields.")

    def __del__(self):
        self.db_connection.close()
        # pass
            
def main():
    root = tk.Tk()
    root.title("Notepad App")
    
    login_app = LoginFrame(root)

    root.mainloop()

if __name__ == "__main__":
    main() 
