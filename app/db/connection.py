from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, registry

DB_URL = config('DATABASE_URL')

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
