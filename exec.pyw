from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import ttk
from models.user import User
from models.book import Book
from back import initDB
from back import getById
from back import getUsersByName
from back import getBooksByName
from back import addUser
from back import updateUser
from back import deleteUser
from back import addBook
from back import updateBook
from back import deleteBook

master = Tk()
master.geometry('500x500')
master.maxsize(500, 500)
master.minsize(500, 500)
master.title('Digital Library')
# INITIALIZATION OF DATABASE
initDB(True)

book_filter_inside = StringVar(master)
book_entry = StringVar(master)
user_filter_inside = StringVar(master)
user_entry = StringVar(master)

def buildItemWindow(item, cls, deleteFun=None, updateFun=None):
	if item['id'] == None and 'book_id' in item:
		item.pop('book_id')
	slave = Toplevel()
	height = 50+51*(len(item.keys()) - 1) - len(item.keys())
	slave.geometry('240x'+str(height))
	slave.maxsize(240, height)
	slave.minsize(240, height)

	ttk.Label(slave, text=cls.__name__+' Info').pack(pady=(5, 0))
	data_frame = ttk.Frame(slave)
	var = {}
	for i in item.keys():
		var[i] = StringVar()
		var[i].set(str(item[i]) if item[i] != None else '')
	for i in item.keys():
		if i != 'id':
			meta_frame = ttk.Frame(data_frame)
			ttk.Label(meta_frame, text=f'{i}:'.replace('_', ' ').title()).pack(anchor='w')
			ttk.Entry(meta_frame, textvariable=var[i]).pack(anchor='w')
			meta_frame.pack(padx=20)
	data_frame.pack(fill='x')

	function_frame = ttk.Frame(slave)
	if item['id'] == None:
		def updateWrap():
			for i in var.keys():
				var[i] = var[i].get()
				var[i] = var[i] if len(var[i].strip()) != 0 else None
			var.pop('id')
			updateFun(var)
			slave.destroy()
		ttk.Button(function_frame, text='Save', command=updateWrap).pack(padx=(5, 10), pady=10)
	else:
		def deleteWrap():
			deleteFun(item['id'])
			slave.destroy()
		def updateWrap():
			for i in var.keys():
				var[i] = var[i].get()
				var[i] = var[i] if len(var[i].strip()) != 0 else None
			var.pop('id')
			updateFun(item['id'], var)
			slave.destroy()
		ttk.Button(function_frame, text='Delete', command=deleteWrap).pack(side='left', padx=(10, 5), pady=10)
		ttk.Button(function_frame, text='Update', command=updateWrap).pack(side='right', padx=(5, 10), pady=10)
	function_frame.pack()

	slave.mainloop()

def getUserByIdCall():
	id = simpledialog.askinteger('Digital Library', 'Input user ID')
	if id != None and (ret:=getById(User, id)) != None:
		buildItemWindow(ret, User, deleteUser, updateUser)
	else:
		messagebox.showerror('Digital Library', 'No Data')

def addUserCall():
	buildItemWindow({'id': None, 'name': None, 'address': None, 'phone': None, 'occupation': None, 'birth': None, 'book_id': None}, User, deleteUser, addUser)

def getBookByIdCall():
	id = simpledialog.askinteger('Digital Library', 'Input book ID')
	if id != None and (ret:=getById(Book, id)) != None:
		buildItemWindow(ret, Book, deleteBook, updateBook)
	else:
		messagebox.showerror('Digital Library', 'No Data')

def addBookCall():
		buildItemWindow({'id': None, 'name': None, 'author': None, 'description': None, 'year': None, 'category': None}, Book, deleteBook, addBook)

def buildMenu():
	menu = Menu(master)
	user_menu = Menu(menu, tearoff=0)
	user_menu.add_command(label='Get user by ID', command=getUserByIdCall)
	user_menu.add_separator()
	user_menu.add_command(label='Add user', command=addUserCall)
	menu.add_cascade(label='User', menu=user_menu)
	book_menu = Menu(menu, tearoff=0)
	book_menu.add_command(label='Get book by ID', command=getBookByIdCall)
	book_menu.add_separator()
	book_menu.add_command(label='Add book', command=addBookCall)
	menu.add_cascade(label='Book', menu=book_menu)
	master.config(menu=menu)

def buildBookSearch():
	filtered_frame = ttk.Frame(master)
	scroll = ttk.Scrollbar(filtered_frame)
	scroll.pack(side='right', fill='y')
	filtered = Listbox(filtered_frame, yscrollcommand=scroll.set)
	filtered.pack(fill='x', expand=1, padx=(5, 0))

	def wrapperSearch():
		ret = getBooksByName(book_entry.get().strip())
		filtered.delete(0, 'end')
		for i in ret:
			filtered.insert('end', f"{i['id']}. {i['name']} | Author: {i['author']} | Year: {i['year']} | Category: {i['category']}")

	search_frame = ttk.Frame(master)
	ttk.Label(master, text='Search BOOKS by name').pack(pady=(5, 0))
	ttk.Entry(search_frame, textvariable=book_entry).pack(side='left', fill='x', expand=1, padx=(5, 0))
	ttk.Button(search_frame, text='search', command=wrapperSearch).pack(side='left', padx=(0, 5))
	search_frame.pack(fill='x')
	
	filtered_frame.pack(fill='x')

def buildUserSearch():
	filtered_frame = ttk.Frame(master)
	scroll = ttk.Scrollbar(filtered_frame)
	scroll.pack(side='right', fill='y')
	filtered = Listbox(filtered_frame, yscrollcommand=scroll.set)
	filtered.pack(fill='x', expand=1, padx=(5, 0))

	def wrapperSearch():
		ret = getUsersByName(user_entry.get().strip())
		filtered.delete(0, 'end')
		for i in ret:
			filtered.insert('end', f"{i['id']}. {i['name']} | Phone: {i['phone']} | Occupation: {i['occupation']} | Book: "+('No Book' if i['book_id'] == None else str(i['book_id']) + ". book"))

	search_frame = ttk.Frame(master)
	ttk.Label(master, text='Search USERS by name').pack(pady=(5, 0))
	ttk.Entry(search_frame, textvariable=user_entry).pack(side='left', fill='x', expand=1, padx=(5, 0))
	ttk.Button(search_frame, text='search', command=wrapperSearch).pack(side='left', padx=(0, 5))
	search_frame.pack(fill='x')

	filtered_frame.pack(fill='x')

buildMenu()
buildBookSearch()
buildUserSearch()

master.mainloop()
