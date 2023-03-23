import sqlalchemy as sql
from utils import meta
from models.user import User
from models.book import Book
from datetime import datetime as dt
from datetime import date

engine = None

def initDB(to_reset=False):
	global engine
	engine = sql.create_engine('sqlite:///storage/database.db')

	if to_reset == True:
		meta.drop_all(engine)
		meta.create_all(engine)

def getById(cls, id):
	cursor = engine.connect()
	with cursor.begin() as trans:
		return cursor.execute(sql.select(cls).where(cls.id==id)).first()

def getBooksByName(name):
	cursor = engine.connect()
	with cursor.begin() as trans:
		return cursor.execute(sql.select(Book).where(Book.name.like(f'%{name}%'))).all()

def getUsersByName(name):
	cursor = engine.connect()
	with cursor.begin() as trans:
		return cursor.execute(sql.select(User).where(User.name.like(f'%{name}%'))).all()
	
def addUser(args):
	cursor = engine.connect()
	with cursor.begin() as trans:
		cursor.execute(sql.insert(User).values(args))

def updateUser(id, args):
	cursor = engine.connect()
	if 'book_id' in args:
		with cursor.begin() as trans:
			if args['book_id'] == None or (cursor.execute(sql.select(User).where(User.book_id==int(args['book_id']))).first() == None and cursor.execute(sql.select(Book).where(Book.id==int(args['book_id']))).first() != None):
				cursor.execute(sql.update(User).where(User.id==id).values(args))

def deleteUser(id):
	cursor = engine.connect()
	with cursor.begin() as trans:
		cursor.execute(sql.delete(User).where(User.id==id))

def addBook(args):
	cursor = engine.connect()
	with cursor.begin() as trans:
		cursor.execute(sql.insert(Book).values(args))

def updateBook(id, args):
	cursor = engine.connect()
	with cursor.begin() as trans:
		cursor.execute(sql.update(Book).where(Book.id==id).values(args))

def deleteBook(id):
	cursor = engine.connect()
	with cursor.begin() as trans:
		cursor.execute(sql.delete(Book).where(Book.id==id))

if __name__=='__main__':
	initDB(True)
