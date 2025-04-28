from tkinter import *
from tkinter import ttk
import sqlite3

root = Tk()
root.title('To-Do List')

#Create the Database

#Create the connector
dataConnector = sqlite3.connect('assignmentData.db')

#Create Cursor
cursor = dataConnector.cursor()

cursor.execute( '''CREATE TABLE IF NOT EXISTS assignmentList(
                    name TEXT,
                    dueDate Text,
                    description TEXT,
                    status TEXT,
                    members TEXT)''')

#Create tree to organize the tasks
columns = ("name", "due","desc", "status", "members")
tree = ttk.Treeview(root, columns = columns, show="headings", height = 15)

tree.heading("name", text = "Task Name")
tree.heading("due", text = "Due Date")
tree.heading("desc", text = "Description")
tree.heading("status", text = "Status")
tree.heading("members", text = "Team Members")

tree.column("name", width = 150)
tree.column("due", width = 150)
tree.column("desc", width = 150)
tree.column("status", width = 150)
tree.column("members", width = 150)

#Click on the task and display task information
def onTreeSelect(event):
    selectedItem = tree.focus()
    task_values = tree.item(selectedItem, 'values')
    if task_values:

        hideActionButtons()
        clearEntryWidgets()
        displayInfoLabelsEntry()

        name_entry.insert(0, task_values[0])
        dueDate_entry.insert(0, task_values[1])
        description_entry.insert(0, task_values[2])
        drop_var.set(task_values[3] if task_values[3] else "Status")
        members_entry.insert(0, task_values[4])

        cancelButton.config(text="Close", command=cancel_action)
        cancelButton.grid(row=6, column=2, padx=5, pady=5, sticky="E")

tree.grid(row=1, column = 0, rowspan = 6, padx = 5, pady = 5)
tree.bind("<<TreeviewSelect>>", onTreeSelect)

################### Functions used throughout the actions #################

#Refresh Assignments
def refreshAssignment():
    for row in tree.get_children():
        tree.delete(row)

    dataConnector = sqlite3.connect('assignmentData.db')
    cursor = dataConnector.cursor()
    #Display the assignments
    cursor.execute("SELECT name, dueDate, description, status, members FROM assignmentList ORDER BY dueDate ASC")
    tasks = cursor.fetchall()
    for task in tasks:
        tree.insert("", END, values = task)
    dataConnector.close()

#Function to display the task information labels and entry widgets
def displayInfoLabelsEntry():
    #Call label and widgets
    name_label.grid(row = 1, column = 1, padx=5, pady=5, sticky ="W")
    dueDate_label.grid(row = 2, column = 1, padx=5, pady=5, sticky ="W")
    description_label.grid(row = 3, column = 1, padx=5, pady=5, sticky ="W")
    members_label.grid(row = 5, column = 1, padx=5, pady=5, sticky ="W")

    name_entry.grid(row = 1, column = 2, padx=5, pady=5)
    dueDate_entry.grid(row = 2, column = 2, padx=5, pady=5)
    description_entry.grid(row = 3, column = 2, padx=5, pady=5)
    drop_menu.grid(row = 4,column = 1,padx=5, pady=5,sticky="W")
    members_entry.grid(row = 5, column = 2, padx=5, pady=5)

#Function to delete the task information labels and entry widgets
def forgetInfoLabelsEntry():
    name_label.grid_forget()
    dueDate_label.grid_forget()
    description_label.grid_forget()
    members_label.grid_forget()

    name_entry.grid_forget()
    dueDate_entry.grid_forget()
    description_entry.grid_forget()
    drop_menu.grid_forget()
    members_entry.grid_forget()

#Function to clear all the entry widgets
def clearEntryWidgets():
        name_entry.delete(0, END)
        dueDate_entry.delete(0, END)
        description_entry.delete(0, END)
        drop_var.set( "Status")
        members_entry.delete(0, END)

#Function to hide the action buttons
def hideActionButtons():
    addButton.grid_forget()
    editButton.grid_forget()
    deleteButton.grid_forget()
    clearButton.grid_forget()   

#use this to queue the UI update after the current event loop finishes
def showActionButtons():
    root.after(0, _show_buttons)

#Function to show the action buttons
def _show_buttons():
    addButton.grid(row = 1, column = 1, padx=5, pady=5)
    editButton.grid(row = 2, column = 1, padx=5, pady=5)
    deleteButton.grid(row = 3, column = 1, padx=5, pady=5)
    clearButton.grid(row = 4, column = 1, padx=5, pady=5)

#################### Functions used to add a task ########################
#Function to add a task into the tree
def add_action():

    hideActionButtons()
    clearEntryWidgets()
    displayInfoLabelsEntry()

    submitButton.config(text="Submit", command=submit_action)
    submitButton.grid(row=6, column=1, padx=5,pady=5, sticky="W")

    cancelButton.config(text="Cancel", command=cancel_action)
    cancelButton.grid(row=6, column=1, padx=5,pady=5, sticky="E")

#Function to submit a task into the tree
def submit_action():
    dataConnector = sqlite3.connect('assignmentData.db')
    cursor = dataConnector.cursor()

    cursor.execute("INSERT INTO assignmentList VALUES(:name,:dueDate,:description,:status,:members)",
        {
            'name':name_entry.get(),
            'dueDate':dueDate_entry.get(),
            'description':description_entry.get(),
            'status':drop_var.get(),
            'members':members_entry.get()
        })

    dataConnector.commit()
    dataConnector.close()

    clearEntryWidgets()
    refreshAssignment()
    forgetInfoLabelsEntry()

    submitButton.grid_forget()
    cancelButton.grid_forget()
    drop_menu.grid_forget()

    showActionButtons()
    root.update()

#Function for the user to cancel adding a task
def cancel_action():
    forgetInfoLabelsEntry()

    submitButton.grid_forget()
    drop_menu.grid_forget()
    cancelButton.grid_forget()
    showActionButtons()

################### Function used to edit a task ########################
currentEditTask = None

def edit_action():
    hideActionButtons()

    assignmentEdit_label.grid(row = 1, column = 1)
    assignmentEdit_entry.grid(row = 2, column = 1)

    submitEditButton.config(text="Load Task", command = loadTask)
    submitEditButton.grid(row=3, column=1, padx=5,pady=5, sticky="E")

    cancelEditButton.config(text="Cancel", command=cancelEdit_action)
    cancelEditButton.grid(row=3, column=1, padx=5,pady=5, sticky="W")
    
def cancelEdit_action():
    assignmentEdit_entry.grid_forget()
    assignmentEdit_label.grid_forget()

    submitEditButton.grid_forget()
    cancelEditButton.grid_forget()
    showActionButtons()

def loadTask():
    assignmentEdit_label.grid_forget()
    assignmentEdit_entry.grid_forget()
    submitEditButton.grid_forget()
    cancelEditButton.grid_forget()

    global currentEditTask
    taskName = assignmentEdit_entry.get().strip()

    taskName = assignmentEdit_entry.get()
    dataConnector = sqlite3.connect('assignmentData.db')
    cursor = dataConnector.cursor()
    cursor.execute("SELECT * FROM assignmentList WHERE LOWER(name) = LOWER(?)", (taskName.lower(),))
    task = cursor.fetchone()
    dataConnector.close()

    if task:
        currentEditTask = task[0]
        displayInfoLabelsEntry()

        clearEntryWidgets()

        name_entry.insert(0, task[0])
        dueDate_entry.insert(0, task[1])
        description_entry.insert(0, task[2])
        drop_var.set(task[3] if task[3] else "Status")
        members_entry.insert(0, task[4])

        submitButton.config(text="Save Changes", command = updateTask)
        submitButton.grid(row=6, column=1, padx=5,pady=5, sticky="E")

        cancelButton.config(text="Cancel", command=cancel_action)
        cancelButton.grid(row=6, column=2, sticky="W")

def updateTask():
    global currentEditTask
    dataConnector = sqlite3.connect('assignmentData.db')
    cursor = dataConnector.cursor()
    cursor.execute(""" 
        UPDATE assignmentList SET
            name = ?,
            dueDate = ?,
            description = ?,
            status = ?,
            members =?
        WHERE LOWER(name) = LOWER(?)                 
""", (
    name_entry.get(),
    dueDate_entry.get(),
    description_entry.get(),
    drop_var.get(),
    members_entry.get(),
    currentEditTask.lower()
))
    dataConnector.commit()
    dataConnector.close()

    currentEditTask = None
    assignmentEdit_entry.delete(0, END)
    forgetInfoLabelsEntry()
    submitButton.grid_forget()
    cancelButton.grid_forget()

    refreshAssignment()
    showActionButtons()

################## Functions used to delete a task #########################

#Function to delete a specific task
def delete_action():
    hideActionButtons()
    #Put the label and entry box for the assignment that is going to be deleted
    assignmentDel_label.grid(row = 1, column = 1)
    assignmentDel_entry.grid(row = 2, column = 1)

    submitDelButton.config(text="Delete Task", command=lambda: confirmDelete(assignmentDel_entry.get()))
    submitDelButton.grid(row=3, column=1, padx=5,pady=5, sticky="E")

    cancelDelButton.config(text="Cancel", command=cancelDelete_action)
    cancelDelButton.grid(row=3, column=1, padx=5,pady=5, sticky="W")

#Function to confirm that the user wants to delete a task
def confirmDelete(taskName):
    taskName = taskName.strip()

    dataConnector = sqlite3.connect('assignmentData.db')
    cursor = dataConnector.cursor()
    #Delete an task
    cursor.execute("DELETE FROM assignmentList WHERE LOWER(name) = LOWER(?)", (taskName,))
    dataConnector.commit()
    dataConnector.close()
    
    assignmentDel_entry.delete(0, END)

    assignmentDel_label.grid_forget()
    assignmentDel_entry.grid_forget()
    submitDelButton.grid_forget()
    cancelDelButton.grid_forget()

    refreshAssignment()
    showActionButtons()
    root.update()

def cancelDelete_action():
    assignmentDel_entry.grid_forget()
    assignmentDel_label.grid_forget()

    submitDelButton.grid_forget()
    cancelDelButton.grid_forget()
    showActionButtons()

################### Function to clear all the tasks #########################
def clear_action():
    dataConnector = sqlite3.connect('assignmentData.db')
    cursor = dataConnector.cursor()
    cursor.execute("DELETE FROM assignmentList")
    dataConnector.commit()
    dataConnector.close()
    refreshAssignment()

################# Creating all the labels, buttons, and widgets ##########################

#Create tree label
tree_label = Label(root, text="\t\t\tTask List", font=("Arial", 25,"bold"))
tree_label.grid(row=0, column=0, padx=5, pady=5, sticky="W")

#Create entry widgets
name_entry = Entry(root, width = 40)
dueDate_entry = Entry(root, width = 40)
description_entry = Entry(root, width = 40)
members_entry = Entry(root, width = 40)

#Label widget
name_label = Label(root, text = "Task Name")
dueDate_label = Label(root, text = "Due Date (yyyy-mm-dd)")
description_label = Label(root, text = "Description")
members_label = Label(root, text = "Members")

#Action buttons
addButton = Button(root, text= "Add Task", command = add_action)
editButton = Button(root, text= "Edit Task", command = edit_action)
deleteButton = Button(root, text= "Delete Task", command = delete_action)
clearButton = Button(root, text= "Clear To-do List", command = clear_action)

#Call action buttons
addButton.grid(row = 1, column = 1, padx=5, pady=5)
editButton.grid(row = 2, column = 1, padx=5, pady=5)
deleteButton.grid(row = 3, column = 1, padx=5, pady=5)
clearButton.grid(row = 4, column = 1, padx=5, pady=5)

#Submit button for adding an assignment
submitButton = Button(root)

#Cancel button to go back to the action buttons
cancelButton = Button(root)

#Cancel button to go back to the action buttons
cancelEditButton = Button(root)

#Cancel button to go back to the action buttons
cancelDelButton = Button(root)

#Label and entry box for deleting an assignment
assignmentDel_label = Label(root, text = "Enter the name of the task you want to delete:")
assignmentDel_entry = Entry(root, width = 40)
submitDelButton = Button(root)

#Label and entry box for deleting an assignment
assignmentEdit_label = Label(root, text = "Enter the name of the task you want to edit:")
assignmentEdit_entry = Entry(root, width = 40)
submitEditButton = Button(root)

#Drop down menu for status
drop_var = StringVar()
drop_var.set("Status")
drop_menu = OptionMenu(root,drop_var,"Not Started", "In Progress")

refreshAssignment()

dataConnector.commit()
dataConnector.close()

root.mainloop()
