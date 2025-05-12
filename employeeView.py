from tkinter import *
from tkinter import ttk
import sqlite3
import subprocess 

root = Tk()
root.title('To-Do List')

# Create the Database
dataConnector = sqlite3.connect('applicationData.db')  # Changed to unified DB
cursor = dataConnector.cursor()

cursor.execute( '''CREATE TABLE IF NOT EXISTS assignmentList(
                    name TEXT,
                    dueDate Text,
                    description TEXT,
                    status TEXT,
                    members TEXT)''')

# Create tree to organize the tasks
columns = ("name", "due", "desc", "status", "members")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)

tree.heading("name", text="Task Name")
tree.heading("due", text="Due Date")
tree.heading("desc", text="Description")
tree.heading("status", text="Status")
tree.heading("members", text="Team Members")

tree.column("name", width=150)
tree.column("due", width=150)
tree.column("desc", width=150)
tree.column("status", width=150)
tree.column("members", width=150)

def refreshAssignment():
    for row in tree.get_children():
        tree.delete(row)

    dataConnector = sqlite3.connect('applicationData.db')
    cursor = dataConnector.cursor()
    
    cursor.execute("SELECT rowid, * FROM assignmentList ORDER BY dueDate ASC")
    tasks = cursor.fetchall()
    for task in tasks:
        # task[0] is rowid, the unique ID in the DB
        tree.insert('', 'end', iid=task[0], values=(task[1], task[2], task[3], task[4], task[5]))
    dataConnector.close()

#Click on the task and display task information
def onTreeSelect(event):
    selectedItem = tree.focus()
    task_values = tree.item(selectedItem, 'values')
    if task_values:
        global selectedTask
        selectedTask = selectedItem

        name_entry.delete(0, END)
        dueDate_entry.delete(0, END)
        description_entry.delete(0, END)
        drop_var.set( "Status")
        members_entry.delete(0, END)
        
        name_label.grid(row = 1, column = 1, padx=5, pady=5, sticky ="W")
        dueDate_label.grid(row = 2, column = 1, padx=5, pady=5, sticky ="W")
        description_label.grid(row = 3, column = 1, padx=5, pady=5, sticky ="W")
        members_label.grid(row = 5, column = 1, padx=5, pady=5, sticky ="W")

        name_entry.grid(row = 1, column = 2, padx=5, pady=5)
        dueDate_entry.grid(row = 2, column = 2, padx=5, pady=5)
        description_entry.grid(row = 3, column = 2, padx=5, pady=5)
        drop_menu.grid(row = 4,column = 1,padx=5, pady=5,sticky="W")
        members_entry.grid(row = 5, column = 2, padx=5, pady=5)

        name_entry.insert(0, task_values[0])
        dueDate_entry.insert(0, task_values[1])
        description_entry.insert(0, task_values[2])
        drop_var.set(task_values[3] if task_values[3] else "Status")
        members_entry.insert(0, task_values[4])

        statusUpdateButton.grid(row=6, column=1, padx=5, pady=5, sticky="W")

        closeButton.config(text="Close", command=close_action)
        closeButton.grid(row=6, column=2, padx=5, pady=5, sticky="E")


tree.grid(row=1, column = 0, rowspan = 6, padx = 5, pady = 5)
tree.bind("<<TreeviewSelect>>", onTreeSelect)

def close_action():
    name_label.grid_forget()
    dueDate_label.grid_forget()
    description_label.grid_forget()
    members_label.grid_forget()

    name_entry.grid_forget()
    dueDate_entry.grid_forget()
    description_entry.grid_forget()
    drop_menu.grid_forget()
    members_entry.grid_forget()

    statusUpdateButton.grid_forget()
    closeButton.grid_forget()


def confirmEdit():
    newStatus = drop_var.get()

    dataConnector = sqlite3.connect('applicationData.db')
    cursor = dataConnector.cursor()
    
    cursor.execute("UPDATE assignmentList SET status = ? WHERE rowid = ?",(newStatus, selectedTask))
    dataConnector.commit()
    dataConnector.close()

    refreshAssignment()
    root.update()

def return_to_login():
    root.destroy()
    subprocess.Popen(['python', 'main.py'])

name_entry = Entry(root, width = 40)
dueDate_entry = Entry(root, width = 40)
description_entry = Entry(root, width = 40)
members_entry = Entry(root, width = 40)

name_label = Label(root, text = "Task Name")
dueDate_label = Label(root, text = "Due Date (yyyy-mm-dd)")
description_label = Label(root, text = "Description")
members_label = Label(root, text = "Members")


statusUpdateButton = Button(root, text= "Update Status")
statusUpdateButton.config(command = confirmEdit)
closeButton = Button(root)

Button(root, text="Logout and Return to Login", command=return_to_login).grid(row=10, column=0, pady=10)

drop_var = StringVar()
drop_var.set("Status")
drop_menu = OptionMenu(root,drop_var,"In Progress", "Complete")

refreshAssignment()

dataConnector.commit()
dataConnector.close()

root.mainloop()
