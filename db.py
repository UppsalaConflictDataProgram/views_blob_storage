import os

from sqlalchemy import create_engine,MetaData
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.orm import relationship

from psycopg2 import connect
from env import env,envpath

meta = MetaData()

engine = create_engine(f"sqlite:///{envpath('DB_FNAME','db.sqlite')}")
Session = sessionmaker(bind=engine)

Base = declarative_base(metadata = meta)

class Blob(Base):
    __tablename__ = "blob"
    id = Column(String,primary_key=True)

class Dgp(Base):
    __tablename__ = "dgp"
    id = Column(Integer,primary_key=True)

class Parameterization(Base):
    __tablename__ = "parameterization"
    id = Column(Integer,primary_key=True)

class Loa(Base):
    __tablename__ = "loa"
    id = Column(Integer,primary_key=True)

class Variable(Base):
    __tablename__ = "variable"
    id = Column(Integer,primary_key=True)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String,unique=True)

Base.metadata.create_all(engine)
