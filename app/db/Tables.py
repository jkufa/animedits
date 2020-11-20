import csv
import os
from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Association Tables
class Edit(Base):
    __tablename__ = "edit"
    id = Column(Integer, primary_key=True)
    url = Column(String(120), unique=True, nullable=False)
    creator_tag = Column(String(30), nullable=False)
    anime_name = Column(String(120), nullable=False, default="")
    song_name = Column(String(120), nullable=False, default="")
    song_artist = Column(String(120), nullable=False, default="")
    black_text = Column(Boolean, nullable=False, default=False)

file_path = os.path.abspath(os.getcwd())+"/app/db/app.db"
engine = create_engine('sqlite:///'+file_path,echo=True)
Base.metadata.create_all(engine)