from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

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

class ParticleSequenceModel(Base):
    __tablename__ = 'particle_sequences'
    id = Column(Integer, primary_key=True)
    sequence_name = Column(String, unique=True)
    map_name = Column(String)
    particle_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    particles = relationship("ParticleDataModel", back_populates="sequence")

class ParticleDataModel(Base):
    __tablename__ = 'particle_data'
    id = Column(Integer, primary_key=True)
    sequence_id = Column(Integer, ForeignKey('particle_sequences.id'))
    particle_index = Column(Integer)
    radius = Column(Float)
    color_r = Column(Integer)
    color_g = Column(Integer)
    color_b = Column(Integer)
    initial_vx = Column(Float)
    sequence = relationship("ParticleSequenceModel", back_populates="particles")

class TestResultModel(Base):
    __tablename__ = 'test_results'
    id = Column(Integer, primary_key=True)
    test_name = Column(String)
    map_name = Column(String)
    sequence_name = Column(String)
    total_time = Column(Float)
    particles_count = Column(Integer)
    particles_per_second = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)