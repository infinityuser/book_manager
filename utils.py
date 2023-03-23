import sqlalchemy as sql
from sqlalchemy import orm

meta = sql.MetaData()
Base = orm.declarative_base(metadata=meta)
