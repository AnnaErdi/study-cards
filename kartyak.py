# -*- coding: utf-8 -*-
"""
Created on Tue Dec 31 17:23:13 2019

@author: Anna
"""

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import csv
import random
import sqlite3
import os

def load():   
    connect = sqlite3.connect('C:/Users/Anna/Documents/INF_Sem_2/Programming II/project 2/demo.db')
    c = connect.cursor()
    c.execute('SELECT * FROM questions')
    all_rows = c.fetchall()

    global lista 
    lista=[]
    for item in all_rows:
        lista.append(item[1])
load()
tab =[]
# ____________________________________________

def pressed(index):
    item = random.choice(lista)
    if item not in tab:
        messagebox.showinfo("Kérdés", item)
        tab.append(item)
    else:
        pressed(index)
   
    buttons[index].configure(bg="#ff944d")
    buttons[index].configure(state=DISABLED)
    
def uj():
    load()
    for floor in floors:
        buttons[floor].configure(bg="#99ccff")
        buttons[floor].configure(state=NORMAL)
    global tab
    tab=[]
    
# _____________________________________________
        
        
def load_to_listbox():
    listbox.delete(0,'end')
    load()
    for line in lista:
        listbox.insert(END, line)

def listbox_click(event):
    # Insert value to entry:
    global selected
    selected = listbox.get(listbox.curselection())
    entry.delete(0, END)
    entry.insert(END, selected)        

def save():
    kerdes = str(entry.get())
    load()
           
    for word in lista:
        if word == selected:
            i = lista.index(word)
            lista[i] = kerdes
            break   # now I have the new lista
            # I just have to add itt to the file (=rewrite it)
             
    with open("kerdesek.txt", "w", encoding="utf-8") as new:
        for line in lista:
            new.write(line+"\n")
        
    load_to_listbox()

def add():
    kerdes = simpledialog.askstring("Kérdés hozzáadása", "Új kérdés:", parent=kerd)
    load()
    lista.append(kerdes)
    
    with open("kerdesek.txt", "w", encoding="utf-8") as new:
        for line in lista:
            new.write(line+"\n") 
        
    load_to_listbox()
    

def delete():
    load() 
            
    for row in lista:
        if row == selected:
            i = lista.index(row)
            del lista[i]
            break
                  
    with open("kerdesek.txt", "w", encoding="utf-8") as new:
        for line in lista:
            new.write(line+"\n")
    entry.delete(0, END)   
    load_to_listbox()    

# _____________________________________________________________
def kerdesek():
    global kerd
    kerd = Tk()
    kerd.title("Kérdések kezelése")
    kerd.geometry("900x450+100+100")
    
    # ============= Add course ============= #
    add_course = Button(kerd, text = "Új kérdés hozzáadása", command=add)
    add_course.grid(row=0, column=0, sticky=W, ipadx=5)
    
    # ============= List of question ============= #
    frame = Frame (kerd)
    frame.grid(row = 1, column = 0, rowspan = 3)
    global listbox
    listbox = Listbox (frame, width=50, height=25)
    listbox.pack(side="left", fill="both")
    listbox.bind("<ButtonRelease-1>", listbox_click) # binding event
    
    scrollbar = Scrollbar(frame, orient="vertical")
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scrollbar.set)
    
    # ============= Kiválasztott kérdés: ============= #
    label_name = Label(kerd, text="Kiválasztott kérdés:   ")
    label_name.grid(row=1, column=1, sticky=S)
    # ============= kerdes editor ============= #
    global entry
    entry = Entry(kerd, width=70)
    entry.grid(row=1, column=2, ipady=6, sticky=S, columnspan=3)
    # ============= Mentés ============= #
    global mentes
    mentes = Button(kerd, text = "Mentés", command=save)
    mentes.grid(row=2, column=2, ipadx=5, sticky=N+E)
    # ============= Törlés ============= #
    global torles
    torles = Button(kerd, text = "Törlés", command=delete)
    torles.grid(row=2, column=3,ipadx=5, sticky=N+W)
    
    vissza = Button(kerd, text="Vissza", command=kerd.destroy)
    vissza.grid(row=3, column=4, sticky=E+S, ipadx=5)
    
    load_to_listbox()
    
    mainloop()    
        
#-------------------------------------------------------------------#  
#                           Tkinter GUI                             #
#-------------------------------------------------------------------#
root = Tk()
root.title("Card Game")
root.geometry("750x490+50+50")

menubar= Menu(root) 
file = Menu(menubar, tearoff=0)  
menubar.add_cascade(label="File", menu=file) 
root.config(menu=menubar)

# Adding the choices within the file menu:
file.add_command(label="Új leosztás", command=uj)
file.add_command(label="Kérdések kezelése", command=kerdesek)
file.add_separator()
file.add_command(label="Kilépés", command=root.destroy)


floors = [i for i in range(1, 31)]
buttons = {}
x = 0
y = 0
for floor in floors:
    if(y%6==0):
        y = 0
        x = x + 1
        
    buttons[floor] = Button(root, width=3, text=str(floor)+".", bg="#99ccff", font=20, 
        command = lambda f=floor: pressed(f))
    
    buttons[floor].grid(row=x, column =y, padx=15, pady=15, ipadx=25, ipady=12)
    y = y+1 
    
# for 60 questions:
# floors = [i for i in range(1, 61)]
# buttons = {}
# x = 0
# y = 0
# for floor in floors:
#     if(y%10==0):
#         y = 0
#         x = x + 1
        
#     buttons[floor] = Button(root, width=3, text=str(floor)+".", bg="#99ccff", font=20, 
#         command = lambda f=floor: pressed(f))
    
#     buttons[floor].grid(row=x, column =y, padx=15, pady=15, ipadx=25, ipady=12)
#     y = y+1 
    
mainloop()


