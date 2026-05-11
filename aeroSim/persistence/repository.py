import os
import ctypes
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from aeroSim.persistence.models import Base, MapModel, PresetModel

class PersistenceRepository:
    def __init__(self, db_path="sqlite:///data/sim_data.db"):
        os.makedirs("data", exist_ok=True)
        self.engine = create_engine(db_path)
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self._init_defaults()

    def _init_defaults(self):
        user32 = ctypes.windll.user32
        w = user32.GetSystemMetrics(0)
        h = user32.GetSystemMetrics(1)
        gap = w * 0.25

        with self.Session() as session:
            if not session.query(MapModel).first():
                ramps = [
                    MapModel(name="default", x_start=20, y_start=h*0.2, x_end=w-gap, y_end=h*0.4),
                    MapModel(name="default", x_start=w-20, y_start=h*0.4, x_end=gap, y_end=h*0.6),
                    MapModel(name="default", x_start=20, y_start=h*0.6, x_end=w-gap, y_end=h*0.8),

                    MapModel(name="funnel", x_start=20, y_start=h*0.1, x_end=w*0.46, y_end=h*0.6),
                    MapModel(name="funnel", x_start=w-20, y_start=h*0.1, x_end=w*0.54, y_end=h*0.6),
                    
                    MapModel(name="funnel", x_start=w*0.41, y_start=h*0.6, x_end=w*0.41, y_end=h*0.95),
                    MapModel(name="funnel", x_start=w*0.59, y_start=h*0.6, x_end=w*0.59, y_end=h*0.95),

                    MapModel(name="funnel", x_start=w*0.41, y_start=h*0.65, x_end=w*0.53, y_end=h*0.7),
                    MapModel(name="funnel", x_start=w*0.59, y_start=h*0.72, x_end=w*0.47, y_end=h*0.77),
                    MapModel(name="funnel", x_start=w*0.41, y_start=h*0.79, x_end=w*0.53, y_end=h*0.84),
                    MapModel(name="funnel", x_start=w*0.59, y_start=h*0.86, x_end=w*0.47, y_end=h*0.91),

                    MapModel(name="dk2", x_start=20, y_start=h*0.2, x_end=w*0.4, y_end=h*0.28),
                    MapModel(name="dk2", x_start=w*0.408, y_start=h*0.282, x_end=w-gap, y_end=h*0.4),
                    MapModel(name="dk2", x_start=w*0.6, y_start=h*0.27, x_end=w*0.6, y_end=h*0.34),
                    
                    MapModel(name="dk2", x_start=w-20, y_start=h*0.4, x_end=w*0.6, y_end=h*0.5),
                    MapModel(name="dk2", x_start=w*0.592, y_start=h*0.502, x_end=gap, y_end=h*0.6),
                    MapModel(name="dk2", x_start=w*0.35, y_start=h*0.55, x_end=w*0.35, y_end=h*0.48),

                    MapModel(name="dk2", x_start=20, y_start=h*0.6, x_end=w*0.3, y_end=h*0.7),
                    MapModel(name="dk2", x_start=w*0.3, y_start=h*0.7, x_end=w*0.31, y_end=h*0.68),
                    MapModel(name="dk2", x_start=w*0.31, y_start=h*0.68, x_end=w*0.32, y_end=h*0.706),
                    MapModel(name="dk2", x_start=w*0.32, y_start=h*0.706, x_end=w-gap, y_end=h*0.85),
                ]
                session.add_all(ramps)
            if not session.query(PresetModel).first():
                preset = PresetModel(name="default", spawn_interval=0.04)
                session.add(preset)
            session.commit()

    def get_maps(self, name="default"):
        with self.Session() as session:
            return session.query(MapModel).filter_by(name=name).all()

    def get_preset(self, name="default"):
        with self.Session() as session:
            return session.query(PresetModel).filter_by(name=name).first()