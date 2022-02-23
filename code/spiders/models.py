from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text, Numeric)
from scrapy.utils.project import get_project_settings


Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    """"""
    Base.metadata.create_all(engine)

# Data Model for DB
class article_db(Base):

    __tablename__="article_db"

    id = Column(Integer, primary_key=True)
    Title = Column(String(), unique=False, nullable=False)
    Author= Column(String(), unique=False, nullable=True)
    Publisher= Column(String(), unique=False, nullable=True)
    Publish_date = Column(Date, unique=False, nullable = False)
    URL = Column(String(), nullable=True, unique=True)
    Summary = Column(String(), unique=False, nullable=True)
    Valence_eval = Column(String(), unique=False, nullable=True)
    Subjective_eval = Column(String(), unique=False, nullable=True)
    Valence_score = Column(Numeric(), unique=False, nullable=True)
    Subjective_score = Column(Numeric(), unique=False, nullable=True)
    Keyword_1 = Column(String(), unique=False, nullable=True)
    Keyword_2 = Column(String(), unique=False, nullable=True)
    Keyword_3 = Column(String(), unique=False, nullable=True)
    Keyword_4 = Column(String(), unique=False, nullable=True)
    Keyword_5 = Column(String(), unique=False, nullable=True)
