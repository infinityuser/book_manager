import sqlalchemy as sql
from utils import Base

class Book(Base):
	__tablename__ = 'books'
	id = sql.Column(sql.Integer, primary_key=True)
	name = sql.Column(sql.Text, nullable=False)
	author = sql.Column(sql.Text, nullable=False)
	description = sql.Column(sql.Text, nullable=False)
	year = sql.Column(sql.Text, nullable=False)
	category = sql.Column(sql.Text, nullable=False)
