from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ

Base = declarative_base()

engine = create_engine(environ.get('USERS_DB_URL'), echo=False)
DBSession = sessionmaker(bind=engine)
Base = declarative_base()