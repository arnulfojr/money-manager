from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from settings import DB_URI
from settings import DB_ECHO


engine = create_engine(
        DB_URI,
        echo=DB_ECHO,
        convert_unicode=True,
        poolclass=NullPool)

Session = sessionmaker(bind=engine, autocommit=False, autoflush=True, expire_on_commit=False)
session = scoped_session(Session)


Model = declarative_base()

