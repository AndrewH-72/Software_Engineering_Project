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
        })
    
    dataConnector.commit()
    dataConnector.close()

    name_entry.delete(0, END)
    dueDate_entry.delete(0, END)
    description_entry.delete(0, END)

    refreshAssignment()

def refreshAssignment():
    dataConnector = sqlite3.connect('assignmentData.db')
    cursor = dataConnector.cursor()

    cursor.execute("SELECT *, oid FROM assignmentList ORDER BY dueDate ASC")
    tasks = cursor.fetchall()
    listbox.delete(0, END)
    for task in tasks:
        listbox.insert(END, f"{task[0]} - {task[1]} - {task[2]} - {task[3]}")
    '''
   show_assignmentList = "\tTasks:\nName:\t\tDue Date:\t\tDescription:\t\tStatus"
    for task in task:
        #show_assignmentList += str(task) + "\n"
        show_assignmentList += f"\n{task[0]}\t\t"
        show_assignmentList += f"{task[1]}\t\t"
        show_assignmentList += f"{task[2]}\t\t"
        show_assignmentList += f"{task[3]}\n"
    '''
    #query_label.config(text=show_assignmentList)
    #query_label = Label(root, text = show_assignmentList)
    dataConnector.close()
    #query_label.grid(row = 6, column = 1)
'''
def refreshAssignment():
    query_assignmentList()
    root.after(1000, refreshAssignment)
'''

def add_action():
    entry()
def edit_action():
    pass
def delete_action():
    pass
def clear_action():
    pass

def rbutton(value):
    #label3 = Label(root, text = f"Selected Status: {value}")
    #label3.grid(row = 4, column = 2, sticky = W, padx = 5)
    pass

#Create GUI
Radio_var = StringVar()
'''

options = ["Not Started", "In Progess", "Complete"]
counter = 0
for option in options:
    Radiobutton(root, text=option, variable = Radio_var, value=option, command=lambda: rbutton(Radio_var.get())).grid(row =3, column = counter+1)
    counter += 1
'''

listbox_label = Label(root, text="Task List", font=("Arial", 14,"bold"))
listbox_label.grid(row=0, column=0, padx=5, pady=5, sticky="W")

listbox = Listbox(root, width=60, height=15)
listbox.grid(row=1, column=0, rowspan=6, padx=5, pady=5)


#Create widgets
name_entry = Entry(root, width = 40)
dueDate_entry = Entry(root, width = 40)
description_entry = Entry(root, width = 40)


#Lable widget
name_label = Label(root, text = "Assignment Name")
dueDate_label = Label(root, text = "Due Date (yy-mm-dd)")
description_label = Label(root, text = "Description")
status_label = Label(root, text = "Status")


#entry = Button(root, text= "Add assignment to To-do list", command = entry)
#show = Button(root, text= "Show list of assignments", command = query_assignmentList)

query_label = Label(root, text="", justify=LEFT)
''' 
#Call entry widgets
name_entry.grid(row = 0, column = 1)
dueDate_entry.grid(row = 1, column = 1)
description_entry.grid(row = 2, column = 1)

#Call label widgets
name_label.grid(row = 0, column = 0)
dueDate_label.grid(row = 1, column = 0)
description_label.grid(row = 2, column = 0)
status_label.grid(row = 3, column = 0)
'''

addButton = Button(root, text= "Add assignment to To-do list", command = add_action)
editButton = Button(root, text= "Edit assignment in To-do list", command = edit_action)
deleteButton = Button(root, text= "Delete assignment to To-do list", command = delete_action)
clearButton = Button(root, text= "Clear To-do list", command = clear_action)

addButton.grid(row = 1, column = 3, padx=5, pady=5)
editButton.grid(row = 2, column = 3, padx=5, pady=5)
deleteButton.grid(row = 3, column = 3, padx=5, pady=5)
clearButton.grid(row = 4, column = 3, padx=5, pady=5)

#entry.grid(row = 5, column = 0)
query_label.grid(row=1, column = 3, columnspan=2, sticky="w")
refreshAssignment()
#show.grid(row = 5, column = 1)

dataConnector.commit()
dataConnector.close()

root.mainloop()
