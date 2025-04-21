from tkinter import *
import sqlite3
import subprocess

#main window
root = Tk()
root.title('User Management System')
root.geometry("400x400")

# Database  
dataConnector = sqlite3.connect('userData.db')
cursor = dataConnector.cursor()


cursor.execute(""" CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    role TEXT
)""")
dataConnector.commit()
dataConnector.close()

# --Functions--
# switching screens
def show_screen(screen):
    add_user_frame.pack_forget()
    login_frame.pack_forget()
    welcome_frame.pack_forget()
    screen.pack(pady=20)

# adding user
def submit():
    dataConnector = sqlite3.connect('userData.db')
    cursor = dataConnector.cursor()
    
    selected_role = role_var.get()
    cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
    (username_entry.get(), password_entry.get(), selected_role))

    dataConnector.commit()
    dataConnector.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)

# show users
def query_users():
    dataConnector = sqlite3.connect('userData.db')
    cursor = dataConnector.cursor()

    cursor.execute("SELECT username, role FROM users")
    persons = cursor.fetchall()

    show_contacts = "Username | Role\n"
    show_contacts += "-" * 20 + "\n"
    for person in persons:
        show_contacts += f"{person[0]} | {person[1]}\n"

    show_users_label.config(text=show_contacts)  

    dataConnector.close()

# clear
def clear_database():
    dataConnector = sqlite3.connect('userData.db')
    cursor = dataConnector.cursor()
    cursor.execute("DELETE FROM users")
    dataConnector.commit()
    dataConnector.close()

# login 
def login():
    dataConnector = sqlite3.connect('userData.db')
    cursor = dataConnector.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                   (login_username.get(), login_password.get()))
    user = cursor.fetchone()

    if user:
        login_result.config(text="")
        welcome_label.config(text=f"Successfully Logged in\nWelcome {user[1]} - {user[3]}")
        show_screen(welcome_frame)
    else:
        login_result.config(text="Invalid username or password!")

    dataConnector.close()

#testing opening the task manager thing
def launch_task_ui():
    try:
        subprocess.Popen(['python', 'test.py'])  
    except Exception as e:
        print('Error launching task UI:', e)

# Welcome Screen
welcome_frame = Frame(root)
welcome_label = Label(welcome_frame, text="")
welcome_label.pack()

# add Userss
add_user_frame = Frame(root)
Label(add_user_frame, text="Username").grid(row=0, column=0)
Label(add_user_frame, text="Password").grid(row=1, column=0)

username_entry = Entry(add_user_frame, width=30)
password_entry = Entry(add_user_frame, width=30)
username_entry.grid(row=0, column=1)
password_entry.grid(row=1, column=1)

role_var = StringVar(value="User")
Radiobutton(add_user_frame, text="Admin", variable=role_var, value="Admin").grid(row=2, column=0)
Radiobutton(add_user_frame, text="User", variable=role_var, value="User").grid(row=2, column=1)

Button(add_user_frame, text="Add User", command=submit).grid(row=3, column=0)
Button(add_user_frame, text="Show Users", command=query_users).grid(row=4, column=0)
Button(add_user_frame, text="Clear Users", command=clear_database).grid(row=5, column=0)

show_users_label = Label(add_user_frame, text="")
show_users_label.grid(row=6, column=0, columnspan=2)

# login
login_frame = Frame(root)
Label(login_frame, text="Username").grid(row=0, column=0)
Label(login_frame, text="Password").grid(row=1, column=0)

login_username = Entry(login_frame, width=30)
login_password = Entry(login_frame, width=30, show="*")
login_username.grid(row=0, column=1)
login_password.grid(row=1, column=1)

Button(login_frame, text="Login", command=login).grid(row=2, column=0, columnspan=2)
login_result = Label(login_frame, text="")
login_result.grid(row=3, column=0, columnspan=2)

# navigation 
nav_frame = Frame(root)
Button(nav_frame, text="Go to Login", command=lambda: show_screen(login_frame)).pack(side=LEFT, padx=10)
Button(nav_frame, text="Go to Add User", command=lambda: show_screen(add_user_frame)).pack(side=RIGHT, padx=10)
nav_frame.pack()

#To do list interaction
Button(welcome_frame, text="Open To Do list", command=launch_task_ui).pack(pady=10)

#  default screen
show_screen(add_user_frame)
root.mainloop()