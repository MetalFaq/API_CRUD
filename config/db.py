#MySQL connection
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# source: https://docs.sqlalchemy.org/en/14/core/engines.html
# source: https://docs.sqlalchemy.org/en/14/glossary.html#term-DBAPI
'''the create_engine() URL: mysql+pymysql:// refers to the pymysql DBAPI/dialect combination'''
'''DBAPI: Python DataBase API Specification'''

#source: https://www.geeksforgeeks.org/connecting-to-sql-database-using-sqlalchemy-in-python/
# DEFINE THE DATABASE CREDENTIALS
# user = 'root'
# password = 'password'
# host = '127.0.0.1'
# port = 8000
# database = 'crud'

def get_connection():
    return create_engine("sqlite:///./crud.db", connect_args = {"check_same_thread": False}) # option 2
# engine = create_engine("sqlite:///./crud.db") # option 2
# create_engine(url = "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database)) # option 1

# The above engine creates a Dialect object tailored towards MySQL, as well
# as a Pool object which will establish a DBAPI connection to a localhost when a connection
# request is first received. 
# The Engine and its underlying Pool do not establish the first actual DBAPI connection until the 
# engine.connect() method is called, or an operation which is dependent on this method such as engine.execute()
# is invoked. 
# 
# The Engine, once created, can either be used directly to interact with the DB, or can be passed to a Session object to work with the ORM. 

engine = get_connection()
meta = MetaData()
# conn = engine.connect('crud.db')

SessionLocal =sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()