import sqlalchemy as sql
from utils import Base

class User(Base):
	__tablename__ = 'users'
	id = sql.Column(sql.Integer, primary_key=True)
	name = sql.Column(sql.Text, nullable=False)
	address = sql.Column(sql.Text, nullable=False)
	phone = sql.Column(sql.Text, nullable=False)
	occupation = sql.Column(sql.Text, nullable=False)
	birth = sql.Column(sql.Text, nullable=False)
	book_id = sql.Column(sql.Integer, sql.ForeignKey('books.id'))
