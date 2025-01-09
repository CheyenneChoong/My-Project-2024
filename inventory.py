#Import modules.
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

#Base window.
window = tk.Tk()
window.title("Inventory")
window.geometry("900x450")

#Navigation.
navbg = tk.Frame(window, bg = "#163E64", width = 180, height = 450)
navbg.place(x = 0, y = 0)
title = tk.Label(navbg, text = "INVENTORY", font = "Tahoma 16 bold", fg = "white", bg = "#163E64")
title.place(x = 0, y = 10, width = 180)
button1 = tk.Button(navbg, text = "ADD CATEGORY", font = "Arial 10 bold", fg = "black", bg = "#E1F3FF")
button1.place(x = 15, y = 60, width = 150, height = 35)
button2 = tk.Button(navbg, text = "ADD ITEM", font = "Arial 10 bold", fg = "black", bg = "#E1F3FF")
button2.place(x = 15, y = 120, width = 150, height = 35)
button3 = tk.Button(navbg, text = "INVENTORY LIST", font = "Arial 10 bold", fg = "black", bg = "#E1F3FF")
button3.place(x = 15, y = 180, width = 150, height = 35)
main_frame = tk.Frame(window, bg  = "white", width = 770, height = 450)
main_frame.place(x = 180, y = 0)

#Widgets List.
#Widgets for Add Category.
addcategory_frame = tk.Frame(window, bg = "white", width = 770, height = 450)
pagetitle1 = tk.Label(main_frame, text = "ADD CATEGORY", font = "Tahoma 16 bold", fg = "black", bg = "white")
categorynamelb = tk.Label(main_frame, text = "Name", font = "Arial 11", fg = "black", bg = "white")
categoryentry = tk.Entry(main_frame, borderwidth = 1, relief = "solid", font = "Arial 10")
addcategorybtn = tk.Button(main_frame, text = "ADD", font = "Arial 10 bold", fg = "white", bg = "#00B050")
updatecategorybtn = tk.Button(main_frame, text = "UPDATE", font = "Arial 10 bold", fg = "white", bg = "#3121FF")
deletecategorybtn = tk.Button(main_frame, text = "DELETE", font = "Arial 10 bold", fg = "white", bg = "#FF0000")
categorylistframe = ttk.Treeview(main_frame, columns = ('category', 'amount'), show = 'headings')
categorylistframe.heading('category', text = "Category")
categorylistframe.heading('amount', text = "Amount of Items")
#Widgets for Add Item Page.
additem_frame = tk.Frame(window, bg = "white", width = 770, height = 450)
pagetitle2 = tk.Label(main_frame, text = "ADD ITEM", font = "Tahoma 16 bold", fg = "black", bg = "white")
itemnamelb = tk.Label(main_frame, text = "Name", font = "Arial 11", fg = "black", bg = "white")
itementry = tk.Entry(main_frame, borderwidth = 1, relief = "solid", font = "Arial 10")
itementrylb = tk.Label(main_frame, text = "Category", font = "Arial 11", fg = "black", bg = "white")
itemcategory = ttk.Combobox(main_frame, font = "Arial 10", state = "readonly")
unitlb = tk.Label(main_frame, text = "Unit Measure", font = "Arial 11", fg = "black", bg = "white")
units = ['number', 'percentage']
unitentry = ttk.Combobox(main_frame, values = units, font = "Arial 10", state = "readonly")
itemquantitylb = tk.Label(main_frame, text = "Quantity", font = "Arial 11", fg = "black", bg = "white")
itemquantityentry = tk.Entry(main_frame, relief = "solid", font = "Arial 10")
additembtn = tk.Button(main_frame, text = "ADD", font = "Arial 10 bold", fg = "white", bg = "#00B050")
updateitembtn = tk.Button(main_frame, text = "UPDATE", font = "Arial 10 bold", fg = "white", bg = "#3121FF")
deleteitembtn = tk.Button(main_frame, text = "DELETE", font = "Arial 10 bold", fg = "white", bg = "#FF0000")
itemlistframe = ttk.Treeview(main_frame, columns = ('name', 'quantity', 'category'), show = 'headings')
itemlistframe.heading('name', text = "Item")
itemlistframe.heading('quantity', text = "Quantity")
itemlistframe.heading('category', text = "Category")
#Widgets for Inventory List Page.
inventorypage_frame = tk.Frame(window, bg = "white", width = 770, height = 450)
pagetitle3 = tk.Label(main_frame, text = "INVENTORY LIST", font = "Tahoma 16 bold", fg = "black", bg = "white")
quantitylb = tk.Label(main_frame, text = "Quantity", font = "Arial 11", fg = "black", bg = "white")
quantityentry = tk.Entry(main_frame, relief = "solid", font = "Arial 10")
updatequantitybtn = tk.Button(main_frame, text = "UPDATE", font = "Arial 10 bold", fg = "white", bg = "#3121FF")
filtercategorylb = tk.Label(main_frame, text = "Category", font = "Arial 11", fg = "black", bg = "white")
filtercategoryentry = ttk.Combobox(main_frame, font = "Arial 10")
inventorylist = ttk.Treeview(main_frame, columns = ('item', 'quantity'), show = 'headings')
inventorylist.heading('item', text = "Item")
inventorylist.heading('quantity', text = "Quantity")

#Connection to database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS category (idcategory INTEGER PRIMARY KEY AUTOINCREMENT, category VARCHAR(255))''')
cursor.execute('''CREATE TABLE IF NOT EXISTS item 
               (iditem INTEGER PRIMARY KEY AUTOINCREMENT,
               idcategory INTEGER,
               item VARCHAR(255),
               measure VARCHAR(255),
               quantity INTEGER,
               FOREIGN KEY (idcategory) REFERENCES category (idcategory))''')

#Variables
selectedidcategory = 0
filteridcategory = 0
selectediditem = 0

#Function to display category in list.
def displaycategory():
    #Fetch data about categories.
    cursor.execute('''SELECT * FROM category''')
    categories = cursor.fetchall()
    #Remove current list (if have)
    for item in categorylistframe.get_children():
        categorylistframe.delete(item)
    #Display latest list
    for category in categories:
        idcategory = category[0]
        categoryname = category[1]
        cursor.execute('''SELECT COUNT(*) FROM item WHERE idcategory = ?''', (idcategory,))
        items = cursor.fetchone()
        categorylistframe.insert(parent = '', index = 'end', iid = idcategory, values = (categoryname, items,))

#Function to display item in list (Add Item Page).
def displayaddeditem():
    #Fetch data about item.
    cursor.execute('''SELECT * FROM item''')
    items = cursor.fetchall()
    #Remove current list (if have)
    for item in itemlistframe.get_children():
        itemlistframe.delete(item)
    #Display latest list.
    for item in items:
        iditem = item[0]
        idcategory = item[1]
        name = item[2]
        quantity = item[4]
        unit = item[3]
        if unit == 'percentage':
            quantity = str(quantity) + "%"
        cursor.execute('''SELECT category FROM category WHERE idcategory = ?''', (idcategory,))
        categoryname = cursor.fetchone()
        categoryname = categoryname[0]
        itemlistframe.insert(parent = '', index = 'end', iid = iditem, values = (name, quantity, categoryname,))

#Function to display inventory in inventory list page.
def displayinventory():
    global filteridcategory
    #Fetch data about items.
    if filteridcategory == 0 :
        cursor.execute('''SELECT * FROM item''')
        items = cursor.fetchall()
    else:
        cursor.execute('''SELECT * FROM item WHERE idcategory = ?''', (filteridcategory,))
        items = cursor.fetchall()
    #Remove current list (if have)
    for item in inventorylist.get_children():
        inventorylist.delete(item)
    #Display latest list.
    for item in items:
        iditem = item[0]
        name = item[2]
        unit = item[3]
        quantity = item[4]
        if unit == 'percentage':
            quantity = str(quantity) + "%"
        inventorylist.insert(parent = '', index = 'end', iid = iditem, values = (name, quantity,))

#Display Pages
#Function to display Add Category Page.
def addcategorypage():
    #Hide the other widgets.
    for fm in main_frame.winfo_children():
        fm.place_forget()
        window.update()

    #Clear any selected category.
    categoryentry.delete(0, tk.END)

    #Positions of all the widgets in this page.
    pagetitle1.place(x = 10, y = 10)
    categorynamelb.place(x = 10, y = 50)
    categoryentry.place(x = 10, y = 80, width = 300)
    addcategorybtn.place(x = 10, y = 110, width = 90)
    updatecategorybtn.place(x = 110, y = 110, width = 90)
    deletecategorybtn.place(x = 210, y = 110, width = 90)
    categorylistframe.place(x = 10, y = 155, width = 700, height = 280)

    #Function to display the category list.
    displaycategory()
#Function to display Add Item Page.
def additempage():
    #Hide the other widgets.
    for fm in main_frame.winfo_children():
        fm.place_forget()
        window.update()
    
    #Get the list of categories.
    cursor.execute('''SELECT category FROM category''')
    categories = cursor.fetchall()
    processed_category = [category[0] for category in categories]
    itemcategory.configure(values = processed_category)

    #Clear any selected items.
    itementry.delete(0, tk.END)
    itemquantityentry.delete(0, tk.END)
    itemcategory.set('')
    unitentry.set('')

    #Position of all the widgets in this page.
    pagetitle2.place(x = 10, y = 10)
    itemnamelb.place(x = 10, y = 50)
    itementry.place(x = 10, y = 80, width = 300)
    itementrylb.place(x = 10, y = 110)
    itemcategory.place(x = 10, y = 140, width = 300)
    unitlb.place(x = 350, y = 50)
    unitentry.place(x = 350, y = 80, width = 300)
    itemquantitylb.place(x = 350, y = 110)
    itemquantityentry.place(x = 350, y = 140, width = 300)
    additembtn.place(x = 10, y = 170, width = 130)
    updateitembtn.place(x = 150, y = 170, width = 130)
    deleteitembtn.place(x = 290, y = 170, width = 130)
    itemlistframe.place(x = 10, y = 210, width = 700, height = 230)

    #Function to display the items.
    displayaddeditem()
#Function to display Inventory List Page.
def inventorylistpage():
    #Reset filter.
    global filteridcategory
    filteridcategory = 0

    #Hide the other widgets.
    for fm in main_frame.winfo_children():
        fm.place_forget()
        window.update()

    #Clear any selection.
    quantityentry.delete(0, tk.END)
    filtercategoryentry.set('')

    #Get the list of categories.
    cursor.execute('''SELECT category FROM category''')
    categories = cursor.fetchall()
    processed_category = [category[0] for category in categories]
    filtercategoryentry.configure(values = processed_category)

    #Positions of the widgets in this page.
    pagetitle3.place(x = 10, y = 10)
    quantitylb.place(x = 10, y = 50, height = 25)
    quantityentry.place(x = 80, y = 50, width = 60, height = 25)
    updatequantitybtn.place(x = 150, y = 50, width = 100, height = 25)
    filtercategorylb.place(x = 300, y = 50, height = 25)
    filtercategoryentry.place(x = 380, y = 50, height = 25, width = 200)
    inventorylist.place(x = 10, y = 90, width = 700, height = 350)

    #Function to display the inventory list.
    displayinventory()

#Functions related to add category page.
#Function to add category into database.
def addcategory():
    category = categoryentry.get()
    if not category:
        messagebox.showerror('Error', 'No category found.')
    else:
        cursor.execute('''SELECT category FROM category WHERE category = ?''',(category,))
        check = cursor.fetchall()
        if not check:
            cursor.execute('''INSERT INTO category (category) VALUES (?)''', (category,))
            addcategorypage()
        else:
            messagebox.showerror('Error', 'Category already exist.')
#On click category.
def onclickcategory(event):
    global selectedidcategory
    for selected in categorylistframe.selection():
        selectedidcategory = selected
        selectedvalues = categorylistframe.item(selected)['values']
        selectedcategory = selectedvalues[0]
        categoryentry.delete(0, tk.END)
        categoryentry.insert(0, selectedcategory)
categorylistframe.bind('<<TreeviewSelect>>', onclickcategory)
#Function to edit category.
def updatecategory():
    global selectedidcategory
    category = categoryentry.get()
    if selectedidcategory == 0:
        messagebox.showerror('Error', "No category selected.")
    else:
        cursor.execute('''UPDATE category SET category = ? WHERE idcategory = ?''', (category, selectedidcategory,))
        selectedidcategory = 0
    addcategorypage()
#Function to delete category.
def delcategory():
    global selectedidcategory
    if selectedidcategory == 0:
        messagebox.showerror('Error', 'No category selected')
    else:
        cursor.execute('''DELETE FROM item WHERE idcategory = ?''', (selectedidcategory,))
        cursor.execute('''DELETE FROM category WHERE idcategory = ?''', (selectedidcategory,))
        selectedidcategory = 0
    addcategorypage()

#Functions related to add item page. 
#Function to add item into database.
def additem():
    name = itementry.get()
    category = itemcategory.get()
    unit = unitentry.get()
    quantity = itemquantityentry.get()

    if not quantity.isdigit():
        messagebox.showerror('Error', 'Please enter a number value for quantity.')
    else:
        if not name or not category or not unit or not quantity:
            messagebox.showerror('Error', 'Fill up all the requirements.')
        else:
            cursor.execute('''SELECT idcategory FROM category WHERE category = ?''', (category,))
            selectedcategory = cursor.fetchall()
            idcategory = [category[0] for category in selectedcategory]
            idcategory = idcategory[0]
            cursor.execute('''INSERT INTO item (idcategory, item, measure, quantity) VALUES (?, ?, ?, ?)''', (idcategory, name, unit, int(quantity),))
            additempage()
#On click add item page.
def onclickadditempage(event):
    global selectediditem
    for selected in itemlistframe.selection():
        selectediditem = selected
        cursor.execute('''SELECT * FROM item WHERE iditem = ?''', (selectediditem,))
        selectedvalues = cursor.fetchone()
        item = selectedvalues[2]
        measure = selectedvalues[3]
        quantity = selectedvalues[4]
        idcategory = selectedvalues[1]
        cursor.execute('''SELECT category FROM category WHERE idcategory = ?''', (idcategory,))
        category = cursor.fetchone()
        category = category[0]
        itementry.delete(0, tk.END)
        itementry.insert(0, item)
        itemquantityentry.delete(0, tk.END)
        itemquantityentry.insert(0, quantity)
        unitentry.set(measure)
        itemcategory.set(category)
itemlistframe.bind('<<TreeviewSelect>>', onclickadditempage)
#Function to update item in add item page.
def updateaddeditem():
    global selectediditem
    name = itementry.get()
    category = itemcategory.get()
    unit = unitentry.get()
    quantity = itemquantityentry.get()

    if selectediditem == 0:
        messagebox.showerror('Error', 'No item selected')
    else:
        if not quantity.isdigit():
            messagebox.showerror('Error', 'Please enter a number value for quantity.')
        else:
            if not name or not category or not unit or not quantity:
                messagebox.showerror('Error', 'Fill up all the requirements.')
            else:
                cursor.execute('''SELECT idcategory FROM category WHERE category = ?''', (category,))
                selectedcategory = cursor.fetchall()
                idcategory = [category[0] for category in selectedcategory]
                idcategory = idcategory[0]
                cursor.execute('''UPDATE item SET idcategory = ?, item = ?, measure = ?, quantity = ? WHERE iditem = ?''', (idcategory, name, unit, int(quantity), selectediditem,))
                selectediditem = 0
                additempage()
#Function to delete item.
def deleteitem():
    global selectediditem

    if selectediditem == 0:
        messagebox.showerror('Error', 'No Item selected')
    else:
        cursor.execute('''DELETE FROM item WHERE iditem = ?''', (selectediditem,))
        selectediditem = 0
        additempage()

#Functions related to inventory list page.
#On click item in inventory list page.
def onclickinventory(event):
    global selectediditem
    for selected in inventorylist.selection():
        selectediditem = selected
        cursor.execute('''SELECT quantity FROM item WHERE iditem = ?''', (selectediditem,))
        selectedquantity = cursor.fetchone()
        quantityentry.delete(0, tk.END)
        quantityentry.insert(0, selectedquantity)
inventorylist.bind('<<TreeviewSelect>>', onclickinventory)
#Update item quantity in inventory list.
def updatequantity():
    global selectediditem
    quantity = quantityentry.get()

    #Check if there's any value.
    if selectediditem == 0:
        messagebox.showerror('Error', 'No item selected.')
    else:
        if not quantity or selectediditem == 0:
            messagebox.showerror('Error', 'No item selected')
        else:
            cursor.execute('''UPDATE item SET quantity = ? WHERE iditem = ?''', (quantity, selectediditem,))
            selectedidtem = 0
            quantityentry.delete(0, tk.END)
            displayinventory()

#Function to filter the items based on categories.
def filteritem(event):
    global filteridcategory
    category = filtercategoryentry.get()
    cursor.execute('''SELECT idcategory FROM category WHERE category = ?''', (category,))
    idcategory = cursor.fetchone()
    idcategory = idcategory[0]

    if not idcategory:
        filteridcategory = 0
    else:
        filteridcategory = idcategory
    
    displayinventory()
filtercategoryentry.bind('<<ComboboxSelected>>', filteritem)

#Configuring the button with the respective functions
button1.configure(command = addcategorypage)
button2.configure(command = additempage)
button3.configure(command = inventorylistpage)
addcategorybtn.configure(command = addcategory)
updatecategorybtn.configure(command = updatecategory)
deletecategorybtn.configure(command = delcategory)
additembtn.configure(command = additem)
updateitembtn.configure(command = updateaddeditem)
deleteitembtn.configure(command = deleteitem)
updatequantitybtn.configure(command = updatequantity)

#Keep window open.
window.resizable(0,0)
window.mainloop()

#Comit and closes the connection to database.
conn.commit()
conn.close()