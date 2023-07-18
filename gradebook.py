import tkinter as tk
from tkinter import *
import time, statistics, pickle, json, csv


verifieduser = {'Admin':'Password'}
Login = False

    
root = Tk()
root.geometry("400x300")
root.title('Gradebook')
root.resizable(0, 0)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
root.config(bg='white')
icon = PhotoImage(file='/home/pi/Bookshelf/PythonCode/grade')                        
root.iconphoto(True,icon)
definitions = {}

class Student_Grades:
        def __init__(self):
            
            try:
                with open('/home/pi/Bookshelf/PythonCode/gradebook/savedgrades.txt','r') as file:
                    data = json.load(file)
                    print('got student records: ' + json.dumps(data))
                    definitions.update(data)
            except Exception as e:
                print('No grade file created yet.')
                # On first run of program the file will fail to open. This is not a concern as after first use the file will be created after the user logs out.
        
        def addgrade():
            gradeaddwindow = Toplevel()
            gradeaddwindow.geometry('500x500')
            gradeaddwindow.title('Add Student Grade')
            def appendd():
                definitions[(name.get())]= (grade.get())
                gradeaddwindow.destroy()
                with open('/home/pi/Bookshelf/PythonCode/gradebook/savedgrades.txt', 'w') as file:
                    file.write(json.dumps(definitions))

            namelabel = Label(gradeaddwindow, text="Student Name: ")
            namelabel.grid(column=1, row=2, sticky=tk.W, padx=5, pady=30)
            name = Entry(gradeaddwindow)
            
            name.grid(column=2, row=2, sticky=tk.E, padx=5, pady=30)
            gradelabel = Label(gradeaddwindow, text="Student Grade:")
            gradelabel.grid(column=1, row=3, sticky=tk.W, padx=5, pady=0)
            grade = Entry(gradeaddwindow)
            
            grade.grid(column=2, row=3, sticky=tk.E, padx=5, pady=5)
            addbutton = Button(gradeaddwindow, text="Submit", command=appendd)
            addbutton.grid(column=3, row=3, sticky=tk.E, padx=5, pady=5)
        
            
def loginscreen():
    
    def logincheck():
        Login = False
        if verifieduser.get(username_entry.get()) == password_entry.get():
            Login = True
            if Login == True:
                root.destroy()
                gradescreen()   
        else:
            Login = False
            print('Login Failed. Check your credentials.')
            faillabel= Label(text='Login Failed. Check your credentials.',fg='red')
            faillabel.grid(column=2, row=4)  
    username_label = Label(root, text="Username:")
    username_label.grid(column=1, row=2, sticky=tk.W, padx=5, pady=30)
    username_entry = Entry(root)
    username_entry.grid(column=2, row=2, sticky=tk.E, padx=5, pady=30)
    password_label = Label(root, text="Password:")
    password_label.grid(column=1, row=3, sticky=tk.W, padx=5, pady=0)
    password_entry = Entry(root,  show="*")
    password_entry.grid(column=2, row=3, sticky=tk.E, padx=5, pady=5)
    login_button = Button(root, text="Login", command=logincheck)
    login_button.grid(column=3, row=3, sticky=tk.E, padx=5, pady=5)

def gradescreen():
    
    Student_Grades()

    gradewindow = Tk()
    gradewindow.title('Gradebook')
    gradewindow.geometry('500x500')
    gradewindow.config(bg='white',)
    welcome = Label(gradewindow, text="Welcome to GradeBook", font = ("Arial",30))
    welcome.grid(pady=30,padx=30)
    optionslabel = Label(gradewindow, text="Click the Options Menu to Start", font = ("Arial",20))
    optionslabel.grid(pady=40,padx=40)
    def logout():
        gradewindow.destroy()
    menubar = Menu(gradewindow, bg='light blue',activebackground='light blue')
    gradewindow.config(menu=menubar)
    fileMenu = Menu(menubar, bg='light blue',activebackground='light blue', tearoff=0)
    menubar.add_cascade(label='Options',menu=fileMenu, font=('arial',15),background='light blue',activebackground='light blue')
    fileMenu.add_separator()
    fileMenu.add_command(label="Add Student",command=Student_Grades.addgrade)
    fileMenu.add_separator()
    fileMenu.add_command(label="View Class Grades", command=showgrades)
    fileMenu.add_separator()
    fileMenu.add_command(label="Remove a Student", command=deletestudent)
    fileMenu.add_separator()
    fileMenu.add_command(label="Logout", command=logout)
    fileMenu.add_separator()
    
    gradewindow.mainloop()
    
def showgrades():
    gradeshow = Toplevel() 
    label = Label(gradeshow, text="Grades", font = ("Arial",20)).grid(row = 0, columnspan = 3)
    Namelabel = Label(gradeshow, text="Name", font = ("Arial",10)).grid(row = 1,column=0 )
    Gradelabel = Label(gradeshow, text="Grade", font = ("Arial",10)).grid(row = 1,column=2)
    Names = Listbox(gradeshow,width = 10)
    Grades = Listbox(gradeshow,width = 10)
    Grades.grid(row= 2, column=2, columnspan= 2)
    for i in definitions:
        Names.insert(END, i)
        Grades.insert(END, definitions[i])
    Names.grid(row = 2,column= 0, columnspan = 2)
    
    

    addbutton = Button(gradeshow, text="Exit", command=gradeshow.destroy)
    addbutton.grid(column=3, row=3, sticky=tk.E, padx=5, pady=5)
def deletestudent():
            deletestudent = Toplevel()
            deletestudent.geometry('500x500')
            deletestudent.title('Delete Student')
            def delete():
                remove = studentpop.get()
                if remove in definitions:
                     definitions.pop(remove)
                elif remove.lower in definitions or remove.upper in definitions:
                     definitions.pop(remove)
                deletestudent.destroy()
                with open('/home/pi/Bookshelf/PythonCode/gradebook/savedgrades.txt', 'w') as file:
                    file.write(json.dumps(definitions))

            namelabel = Label(deletestudent, text="Student Name: ")
            namelabel.grid(column=1, row=2, sticky=tk.W, padx=5, pady=30)
            studentpop = Entry(deletestudent)
            
            studentpop.grid(column=2, row=2, sticky=tk.E, padx=5, pady=30)
            
            addbutton = Button(deletestudent, text="Confirm", command=delete)
            addbutton.grid(column=3, row=3, sticky=tk.E, padx=5, pady=5)   
loginscreen()
root.mainloop()

