import os
import ctypes
import random
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from aeroSim.persistence.models import (
    Base, MapModel, PresetModel, ParticleSequenceModel,
    TestResultModel
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
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        self._migrate_particle_sequence_seed()
        self._migrate_test_result_status()
        self._migrate_preset_friction()
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
                    
                    # default_inclinado (Inclinação dobrada)
                    MapModel(name="default_inclinado", x_start=20, y_start=h*0.05, x_end=w-gap, y_end=h*0.45),
                    MapModel(name="default_inclinado", x_start=w-20, y_start=h*0.45, x_end=gap, y_end=h*0.85),

                    # default_curva_c (Baseado no default_modified + rampas em C)
                    # Rampa 1
                    MapModel(name="default_curva_c", x_start=20, y_start=h*0.2, x_end=w-gap, y_end=h*0.4),
                    # Curva C - Lado Direito
                    MapModel(name="default_curva_c", x_start=w-gap+20, y_start=h*0.35, x_end=w-gap+60, y_end=h*0.42),
                    MapModel(name="default_curva_c", x_start=w-gap+60, y_start=h*0.42, x_end=w-gap+20, y_end=h*0.47),
                    MapModel(name="default_curva_c", x_start=w-gap+20, y_start=h*0.47, x_end=w-gap-20, y_end=h*0.49),
                    # Rampa 2
                    MapModel(name="default_curva_c", x_start=w-gap-20, y_start=h*0.49, x_end=gap, y_end=h*0.65),
                    # Curva C - Lado Esquerdo
                    MapModel(name="default_curva_c", x_start=gap-20, y_start=h*0.6, x_end=gap-60, y_end=h*0.67),
                    MapModel(name="default_curva_c", x_start=gap-60, y_start=h*0.67, x_end=gap-20, y_end=h*0.72),
                    MapModel(name="default_curva_c", x_start=gap-20, y_start=h*0.72, x_end=gap+20, y_end=h*0.74),
                    # Rampa 3
                    MapModel(name="default_curva_c", x_start=gap+20, y_start=h*0.74, x_end=w-gap, y_end=h*0.9),
                ]
                session.add_all(ramps)
            if not session.query(PresetModel).first():
                preset = PresetModel(name="default", spawn_interval=0.05, particle_friction=0.004)
                session.add(preset)
            session.commit()

    def _migrate_particle_sequence_seed(self):
        inspector = inspect(self.engine)
        if 'particle_sequences' not in inspector.get_table_names():
            return

        columns = [column['name'] for column in inspector.get_columns('particle_sequences')]
        if 'seed' in columns:
            return

        seed_map = {
            1000: 123456,
            1500: 234567,
            2000: 345678,
            2500: 456789
        }

        with self.engine.begin() as conn:
            conn.execute(text('ALTER TABLE particle_sequences ADD COLUMN seed INTEGER'))
            for count, seed in seed_map.items():
                conn.execute(
                    text('UPDATE particle_sequences SET seed = :seed WHERE particle_count = :count'),
                    {'seed': seed, 'count': count}
                )

    def _migrate_test_result_status(self):
        inspector = inspect(self.engine)
        if 'test_results' not in inspector.get_table_names():
            return

        columns = [column['name'] for column in inspector.get_columns('test_results')]
        if 'status' in columns:
            return

        with self.engine.begin() as conn:
            conn.execute(text('ALTER TABLE test_results ADD COLUMN status VARCHAR DEFAULT "Concluído"'))

    def _migrate_preset_friction(self):
        inspector = inspect(self.engine)
        if 'presets' not in inspector.get_table_names():
            return

        columns = [column['name'] for column in inspector.get_columns('presets')]
        if 'particle_friction' in columns:
            return

        with self.engine.begin() as conn:
            conn.execute(text('ALTER TABLE presets ADD COLUMN particle_friction FLOAT DEFAULT 0.01'))

    def get_maps(self, name="default"):
        with self.Session() as session:
            return session.query(MapModel).filter_by(name=name).all()

    def get_map_names(self):
        with self.Session() as session:
            names = session.query(MapModel.name).distinct().order_by(MapModel.name).all()
            return [name for (name,) in names]

    def duplicate_map(self, source_name: str, target_name: str):
        with self.Session() as session:
            existing = session.query(MapModel).filter_by(name=target_name).first()
            if existing:
                raise ValueError(f"Mapa '{target_name}' já existe.")

            ramps = session.query(MapModel).filter_by(name=source_name).all()
            if not ramps:
                raise ValueError(f"Mapa de origem '{source_name}' não encontrado.")

            duplicated = []
            for ramp in ramps:
                duplicated.append(MapModel(
                    name=target_name,
                    x_start=ramp.x_start,
                    y_start=ramp.y_start,
                    x_end=ramp.x_end,
                    y_end=ramp.y_end
                ))
            session.add_all(duplicated)
            session.commit()
            return duplicated

    def get_preset(self, name="default"):
        with self.Session() as session:
            return session.query(PresetModel).filter_by(name=name).first()

    def get_all_presets(self):
        with self.Session() as session:
            return session.query(PresetModel).all()

    def save_preset(self, name: str, spawn_interval: float = 0.04, particle_friction: float = 0.01):
        with self.Session() as session:
            preset = session.query(PresetModel).filter_by(name=name).first()
            if not preset:
                preset = PresetModel(name=name, spawn_interval=spawn_interval, particle_friction=particle_friction)
                session.add(preset)
            else:
                preset.spawn_interval = spawn_interval
                preset.particle_friction = particle_friction
            session.commit()
            return preset

    def generate_particle_sequence(self, sequence_name: str, map_name: str, particle_count: int):
        with self.Session() as session:
            existing = session.query(ParticleSequenceModel).filter_by(sequence_name=sequence_name).first()
            if existing:
                return existing

            seed_map = {
                1000: 123456,
                1500: 234567,
                2000: 345678,
                2500: 456789
            }
            seed = seed_map.get(particle_count)
            if seed is None:
                raise ValueError(
                    f"Quantidade de partículas inválida: {particle_count}. "
                    f"Use apenas [1000, 1500, 2000, 2500]."
                )

            seq = ParticleSequenceModel(
                sequence_name=sequence_name,
                map_name=map_name,
                particle_count=particle_count,
                seed=seed
            )
            session.add(seq)
            session.commit()
            return seq

    def get_particle_sequence(self, sequence_name: str):
        with self.Session() as session:
            return session.query(ParticleSequenceModel).filter_by(sequence_name=sequence_name).first()

    def get_sequence_particles(self, sequence_name: str):
        """Compatibilidade: partículas não são mais salvas individualmente."""
        return []

    def save_test_result(self, test_name: str, map_name: str, sequence_name: str,
                         total_time: float, particles_count: int, status: str = 'Concluído'):
        """Salva resultado de um teste"""
        particles_per_second = particles_count / total_time if total_time > 0 else 0
        
        with self.Session() as session:
            result = TestResultModel(
                test_name=test_name,
                map_name=map_name,
                sequence_name=sequence_name,
                total_time=total_time,
                particles_count=particles_count,
                particles_per_second=particles_per_second,
                status=status
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