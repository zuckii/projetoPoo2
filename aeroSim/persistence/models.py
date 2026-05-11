from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MapModel(Base):
    __tablename__ = 'maps'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    x_start = Column(Float)
    y_start = Column(Float)
    x_end = Column(Float)
    y_end = Column(Float)

class PresetModel(Base):
    __tablename__ = 'presets'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    spawn_interval = Column(Float)