from tkinter import *
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

#Create Function
def submit_action():
    dataConnector = sqlite3.connect('assignmentData.db')
    cursor = dataConnector.cursor()

    cursor.execute("INSERT INTO assignmentList VALUES(:name,:dueDate,:description,:status,:members)",
        {
            'name':name_entry.get(),
            'dueDate':dueDate_entry.get(),
            'description':description_entry.get(),
            'status':Radio_var.get(),
            'members':members_entry.get()
        })

    dataConnector.commit()
    dataConnector.close()

    name_entry.delete(0, END)
    dueDate_entry.delete(0, END)
    description_entry.delete(0, END)
    members_entry.delete(0, END)

    refreshAssignment()

    #Hide label and widgets
    name_label.grid_forget()
    dueDate_label.grid_forget()
    description_label.grid_forget()
    status_label.grid_forget()
    members_label.grid_forget()

    name_entry.grid_forget()
    dueDate_entry.grid_forget()
    description_entry.grid_forget()
    members_entry.grid_forget()

    submitButton.grid_forget()
    drop_menu.grid_forget()

def refreshAssignment():
    dataConnector = sqlite3.connect('assignmentData.db')
    cursor = dataConnector.cursor()
    #Display the assignments
    cursor.execute("SELECT *, oid FROM assignmentList ORDER BY dueDate ASC")
    tasks = cursor.fetchall()
    listbox.delete(0, END)
    for task in tasks:
        listbox.insert(END, f"{task[0]} - {task[1]} - {task[2]} - {task[3]}")
    dataConnector.close()

def add_action():
    #Call label and widgets
    name_label.grid(row = 1, column = 1,columnspan = 2, padx=5, pady=5, sticky ="W")
    dueDate_label.grid(row = 2, column = 1, columnspan = 2, padx=5, pady=5, sticky ="W")
    description_label.grid(row = 3, column = 1, columnspan = 2, padx=5, pady=5, sticky ="W")
    #status_label.grid(row = 10, column = 1, columnspan = 2, padx=5, pady=5, sticky ="W")
    members_label.grid(row = 5, column = 1, columnspan = 2, padx=5, pady=5, sticky ="W")

    name_entry.grid(row = 1, column = 2, padx=5, pady=5)
    dueDate_entry.grid(row = 2, column = 2, padx=5, pady=5)
    description_entry.grid(row = 3, column = 2, padx=5, pady=5)
    drop_menu.grid(row = 4,column = 1, sticky="W")
    members_entry.grid(row = 5, column = 2, padx=5, pady=5)

    submitButton.config(text="Submit Assignment", command=submit_action)
    submitButton.grid(row=6, column=1, padx=5,pady=5, sticky="W")





def edit_action():
    pass
def delete_action():
    pass
def clear_action():
    #Clear listbox
    listbox.delete(0,"end")
    #Deletes items from database
    dataConnector = sqlite3.connect('assignmentData.db')
    cursor = dataConnector.cursor()
    cursor.execute("DELETE FROM assignmentList")
    dataConnector.commit()
    dataConnector.close()

    refreshAssignment()

#Create GUI
Radio_var = StringVar()
Radio_var.set("Not Started")

#Create listbox to show assignments
listbox_label = Label(root, text="\t\tTask List", font=("Arial", 25,"bold"))
listbox_label.grid(row=0, column=0, padx=5, pady=5, sticky="W")

listbox = Listbox(root, width=60, height=15)
listbox.grid(row=1, column=0, rowspan=6, padx=5, pady=5)


#Create entry widgets
name_entry = Entry(root, width = 40)
dueDate_entry = Entry(root, width = 40)
description_entry = Entry(root, width = 40)
members_entry = Entry(root, width = 40)

#Label widget
name_label = Label(root, text = "Task Name")
dueDate_label = Label(root, text = "Due Date (yy-mm-dd)")
description_label = Label(root, text = "Description")
status_label = Label(root, text = "Status")
members_label = Label(root, text = "Members")


#Action buttons
addButton = Button(root, text= "Add Task", command = add_action)
editButton = Button(root, text= "Edit Task", command = edit_action)
deleteButton = Button(root, text= "Delete Task", command = delete_action)
clearButton = Button(root, text= "Clear To-do list", command = clear_action)

#Call buttons
addButton.grid(row = 8, column = 0, padx=5, pady=5)
editButton.grid(row = 8, column = 1, padx=5, pady=5)
deleteButton.grid(row = 8, column = 2, padx=5, pady=5)
clearButton.grid(row = 8, column = 3, padx=5, pady=5)

submitButton = Button(root)

drop_var = StringVar()
drop_var.set("Status")
drop_menu = OptionMenu(root,drop_var,"Not Started", "In Progess", "Complete")

refreshAssignment()

dataConnector.commit()
dataConnector.close()

root.mainloop()
