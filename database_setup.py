'''
With this file we are learning how to setup
and create a database in an object-oriented-style
but also using Python. Esentially we need to use
ORM (Object relational mapping) which allows us to
represent database code (like SQL) in python objects

To create a database in Python, these are the four steps
that need to be taken:

Configuration Code
Class Code
Table
Mapper 

'''


# So everything here is configuration code:
import os
import sys

# These will come in handy when running the mapping code
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

# Begin the class code

class Restaurant(Base):
	__tablename__ = 'restaurant'
	
	name = Column(
		String(80), nullable = False)

	id = Column(
		Integer, primary_key = True)

class MenuItem(Base):
	__tablename__ = 'menu_item'

	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	course = Column(String(250))
	description = Column(String)
	price = Column(String)

	restauruant_id = Column(
		Integer, ForeignKey('restaurant.id'))

	restaurant = relationship(Restaurant)

engine = create_engine(
'sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)