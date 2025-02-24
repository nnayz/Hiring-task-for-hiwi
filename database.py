from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
SQLALCHEMY_DATABASE_URL = 'sqlite:///./database.db'
# an SQLite database file is going to be created or used in the current repository

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# Establish a connection to the sqlite database

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # autocommit=False prevents SQLAlchemy to commit
# any changes to the database automatically after any query or data modifications: It is only going to commit when it is explicitly told to

# auto flush=False because it will not automatically flush the pending changes to the database before executing a query


# Allows interactions with the database, like querying and committing transactions
# and it is bound to the engine for enabling communication with the Database

# Session in SQLAlchemy is a temporary workspace that manages the interactions between your Python application and database
# Used to Query the database, track changes, commit transactions, manage database connections

# get_db() function provides a session for each request

Base = declarative_base()
# Provides the necessary functionality to define and map my python classes to database tables