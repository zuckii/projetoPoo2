from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.orm import declarative_base
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
    particle_friction = Column(Float, default=0.01)

class ParticleSequenceModel(Base):
    __tablename__ = 'particle_sequences'
    id = Column(Integer, primary_key=True)
    sequence_name = Column(String, unique=True)
    map_name = Column(String)
    particle_count = Column(Integer)
    seed = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class TestResultModel(Base):
    __tablename__ = 'test_results'
    id = Column(Integer, primary_key=True)
    test_name = Column(String)
    map_name = Column(String)
    sequence_name = Column(String)
    total_time = Column(Float)
    particles_count = Column(Integer)
    particles_per_second = Column(Float)
    status = Column(String, default='Concluído')
    created_at = Column(DateTime, default=datetime.utcnow)


class SimulationResultModel(Base):
    __tablename__ = 'simulation_results'
    id = Column(Integer, primary_key=True)
    execution_name = Column(String)
    map_name = Column(String)
    particles_count = Column(Integer)
    total_time = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)