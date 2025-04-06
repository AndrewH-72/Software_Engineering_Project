from tkinter import *
import sqlite3

root = Tk()
root.title('Assignment Information')

#Create the Database

#Create the connector
dataConnector = sqlite3.connect('assignmentData.db')

#Create Cursor
cursor = dataConnector.cursor()

cursor.execute( '''CREATE TABLE IF NOT EXISTS assignmentList(
                    name TEXT,
                    dueDate Text,
                    description TEXT,
                    status TEXT)
''')

#Create Function
def entry():
    dataConnector = sqlite3.connect('assignmentData.db')
    cursor = dataConnector.cursor()

    cursor.execute("INSERT INTO assignmentList VALUES(:name,:dueDate,:description,:status)",
        {
            'name':name_entry.get(),
            'dueDate':dueDate_entry.get(),
            'description':description_entry.get(),
            'status':Radio_var.get()
        }
        )
    dataConnector.commit()
    dataConnector.close()

    name_entry.delete(0, END)
    dueDate_entry.delete(0, END)
    description_entry.delete(0, END)

def query_assignmentList():
    dataConnector = sqlite3.connect('assignmentData.db')
    cursor = dataConnector.cursor()

    cursor.execute("SELECT *, oid FROM assignmentList ORDER BY dueDate ASC")
    task = cursor.fetchall()

    show_assignmentList = ""
    for task in task:
        show_assignmentList += str(task) + "\n"
    
    query_label = Label(root, text = show_assignmentList)
    query_label.grid(row = 6, column = 1)


def rbutton(value):
    label3 = Label(root, text = f"Selected Status: {value}")
    label3.grid(row = 4, column = 2, sticky = W, padx = 5)

#Create GUI
Radio_var = StringVar()

options = ["Not Started", "In Progess", "Complete"]
counter = 0
for option in options:
    Radiobutton(root, text=option, variable = Radio_var, value=option, command=lambda: rbutton(Radio_var.get())).grid(row =3, column = counter+1)
    counter += 1


#Create widgets
name_entry = Entry(root, width = 50)
dueDate_entry = Entry(root, width = 50)
description_entry = Entry(root, width = 50)


#Lable widget
name_label = Label(root, text = "Assignment Name")
dueDate_label = Label(root, text = "Due Date (yy-mm-dd)")
description_label = Label(root, text = "Description")
status_label = Label(root, text = "Status")


entry = Button(root, text= "Add assignment to To-do list", command = entry)
show = Button(root, text= "Show list of assignments", command = query_assignmentList)


#Call entry widgets
name_entry.grid(row = 0, column = 1)
dueDate_entry.grid(row = 1, column = 1)
description_entry.grid(row = 2, column = 1)

#Call label widgets
name_label.grid(row = 0, column = 0)
dueDate_label.grid(row = 1, column = 0)
description_label.grid(row = 2, column = 0)
status_label.grid(row = 3, column = 0)

entry.grid(row = 5, column = 0)
show.grid(row = 5, column = 1)

dataConnector.commit()
dataConnector.close()

root.mainloop()
