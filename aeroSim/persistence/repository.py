import os
import ctypes
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from aeroSim.persistence.models import Base, MapModel, PresetModel

class PersistenceRepository:
    def __init__(self, db_path="sqlite:///data/sim_data.db"):
        os.makedirs("data", exist_ok=True)
        self.engine = create_engine(db_path)
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

                    MapModel(name="funnel", x_start=20, y_start=h*0.2, x_end=w*0.31, y_end=h*0.2),
                    MapModel(name="funnel", x_start=w*0.3, y_start=h*0.19, x_end=w*0.3, y_end=h*0.31),
                    MapModel(name="funnel", x_start=w*0.29, y_start=h*0.3, x_end=w*0.41, y_end=h*0.3),
                    MapModel(name="funnel", x_start=w*0.4, y_start=h*0.29, x_end=w*0.4, y_end=h*0.41),
                    MapModel(name="funnel", x_start=w*0.39, y_start=h*0.4, x_end=w*0.49, y_end=h*0.4),
                    MapModel(name="funnel", x_start=w*0.48, y_start=h*0.39, x_end=w*0.48, y_end=h*0.61),

                    MapModel(name="funnel", x_start=w-20, y_start=h*0.2, x_end=w*0.69, y_end=h*0.2),
                    MapModel(name="funnel", x_start=w*0.7, y_start=h*0.19, x_end=w*0.7, y_end=h*0.31),
                    MapModel(name="funnel", x_start=w*0.71, y_start=h*0.3, x_end=w*0.59, y_end=h*0.3),
                    MapModel(name="funnel", x_start=w*0.6, y_start=h*0.29, x_end=w*0.6, y_end=h*0.41),
                    MapModel(name="funnel", x_start=w*0.61, y_start=h*0.4, x_end=w*0.51, y_end=h*0.4),
                    MapModel(name="funnel", x_start=w*0.52, y_start=h*0.39, x_end=w*0.52, y_end=h*0.61),

                    MapModel(name="funnel", x_start=w*0.47, y_start=h*0.45, x_end=w*0.52, y_end=h*0.48),
                    MapModel(name="funnel", x_start=w*0.53, y_start=h*0.50, x_end=w*0.48, y_end=h*0.53),

                    MapModel(name="funnel", x_start=w*0.48, y_start=h*0.59, x_end=w*0.495, y_end=h*0.8),
                    MapModel(name="funnel", x_start=w*0.52, y_start=h*0.59, x_end=w*0.505, y_end=h*0.8),
                ]
                session.add_all(ramps)
            if not session.query(PresetModel).first():
                preset = PresetModel(name="default", spawn_interval=0.05)
                session.add(preset)
            session.commit()

    def get_maps(self, name="default"):
        with self.Session() as session:
            return session.query(MapModel).filter_by(name=name).all()

    def get_preset(self, name="default"):
        with self.Session() as session:
            return session.query(PresetModel).filter_by(name=name).first()