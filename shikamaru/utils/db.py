import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite+pysqlite:///database.db')
Base = declarative_base()
Session = sessionmaker(bind = engine)
session = Session()

class BotData(Base):

	__tablename__ = "botdata"

	id = Column(Integer, primary_key=True)
	command_ran = Column(Integer)

def create_db():
	Base.metadata.create_all(engine)
	init = BotData(command_ran=0)
	session.add(init)
	session.commit()

def increment():
	before = session.query(BotData).first()
	if not before:
		init = BotData(command_ran=1)
		session.add(init)
		session.commit()
		return
	before.command_ran += 1
	session.commit()