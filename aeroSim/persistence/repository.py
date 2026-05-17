import os
import ctypes
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, selectinload
from aeroSim.persistence.models import (
    Base, MapModel, PresetModel, ParticleSequenceModel,
    ParticleDataModel, TestResultModel
)

class PersistenceRepository:
    def __init__(self, db_path="sqlite:///data/sim_data.db", preserve_data: bool = True):
        os.makedirs("data", exist_ok=True)
        self.engine = create_engine(db_path)
        
        # Se preserve_data é False, apaga tudo (para testes limpos)
        if not preserve_data:
            Base.metadata.drop_all(self.engine)
        
        # Sempre cria tabelas se não existirem
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

                    MapModel(name="default_modified", x_start=20, y_start=h*0.2, x_end=w-gap, y_end=h*0.4),
                    MapModel(name="default_modified", x_start=w-20, y_start=h*0.4, x_end=gap, y_end=h*0.6),
                    MapModel(name="default_modified", x_start=20, y_start=h*0.6, x_end=w-gap, y_end=h*0.8),

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

    def generate_particle_sequence(self, sequence_name: str, map_name: str, particle_count: int):
        with self.Session() as session:
            existing = session.query(ParticleSequenceModel).options(
                selectinload(ParticleSequenceModel.particles)
            ).filter_by(sequence_name=sequence_name).first()

            if existing:
                return existing

            seq = ParticleSequenceModel(
                sequence_name=sequence_name,
                map_name=map_name,
                particle_count=particle_count
            )
            session.add(seq)
            session.flush()

            # Determinismo robusto: usar um gerador local `random.Random`
            # seedado com `particle_count` para que a geração dependa
            # apenas da quantidade e não seja afetada pela RNG global.
            rng = random.Random(particle_count)

            for i in range(particle_count):
                particle_data = ParticleDataModel(
                    sequence_id=seq.id,
                    particle_index=i,
                    radius=rng.uniform(3.0, 8.0),
                    color_r=rng.randint(50, 255),
                    color_g=rng.randint(50, 255),
                    color_b=rng.randint(150, 255),
                    initial_vx=rng.uniform(1, 4)
                )
                session.add(particle_data)

            session.commit()

            return session.query(ParticleSequenceModel).options(
                selectinload(ParticleSequenceModel.particles)
            ).filter_by(id=seq.id).first()

    def get_particle_sequence(self, sequence_name: str):
        with self.Session() as session:
            return session.query(ParticleSequenceModel).options(
                selectinload(ParticleSequenceModel.particles)
            ).filter_by(sequence_name=sequence_name).first()

    def get_sequence_particles(self, sequence_name: str):
        """Recupera todos os dados de partículas de uma sequência"""
        with self.Session() as session:
            sequence = session.query(ParticleSequenceModel).filter_by(sequence_name=sequence_name).first()
            if sequence:
                particles = session.query(ParticleDataModel).filter_by(sequence_id=sequence.id).all()
                return particles
            return []

    def save_test_result(self, test_name: str, map_name: str, sequence_name: str,
                         total_time: float, particles_count: int):
        """Salva resultado de um teste"""
        particles_per_second = particles_count / total_time if total_time > 0 else 0
        
        with self.Session() as session:
            result = TestResultModel(
                test_name=test_name,
                map_name=map_name,
                sequence_name=sequence_name,
                total_time=total_time,
                particles_count=particles_count,
                particles_per_second=particles_per_second
            )
            session.add(result)
            session.commit()
            return result

    def get_test_results(self, map_name: str = None):
        """Recupera resultados de testes"""
        with self.Session() as session:
            query = session.query(TestResultModel)
            if map_name:
                query = query.filter_by(map_name=map_name)
            results = query.order_by(TestResultModel.created_at.desc()).all()
            return results

    def get_latest_test_results(self, limit: int = 5):
        """Recupera os últimos resultados de testes"""
        with self.Session() as session:
            results = session.query(TestResultModel).order_by(
                TestResultModel.created_at.desc()
            ).limit(limit).all()
            return results