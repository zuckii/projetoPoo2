from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from aeroSim.persistence.repository import PersistenceRepository
from aeroSim.simulation.simulation import Simulation


@dataclass(slots=True)
class BatchExecutionConfig:
    """Configuração de uma única execução dentro de um lote."""

    execution_name: str
    map_name: str
    particles_count: int
    gravity: float | None = None
    wind_x: float | None = None
    wind_y: float | None = None
    drag_coefficient: float | None = None
    bounce_damping: float | None = None


@dataclass(slots=True)
class SimulationResult:
    """Resultado consolidado de uma execução concluída."""

    execution_name: str
    map_name: str
    particles_count: int
    total_time: float


class BatchSimulationRunner:
    """Orquestra uma sequência de simulações, persistindo apenas o resumo final."""

    def __init__(
        self,
        executions: Sequence[BatchExecutionConfig],
        repository: PersistenceRepository | None = None,
    ) -> None:
        self.executions = list(executions)
        self.repo = repository or PersistenceRepository(preserve_data=True)

    def run(self) -> list[SimulationResult]:
        results: list[SimulationResult] = []

        for execution in self.executions:
            sequence_name = f"batch_seq_{execution.particles_count}"
            self.repo.generate_particle_sequence(sequence_name, execution.map_name, execution.particles_count)

            simulation = Simulation(test_mode=True, create_renderer=True)
            world, solver = simulation.build_runtime(
                map_name=execution.map_name,
                particle_count=execution.particles_count,
                sequence_name=sequence_name,
                gravity=execution.gravity,
                wind_x=execution.wind_x,
                wind_y=execution.wind_y,
                drag_coefficient=execution.drag_coefficient,
                bounce_damping=execution.bounce_damping,
            )

            result_data = simulation.execute_world(
                world=world,
                solver=solver,
                execution_name=execution.execution_name,
                map_name=execution.map_name,
                particles_count=execution.particles_count,
                sequence_name=sequence_name,
                render=True,
                persist_test_result=True,
            )

            result = SimulationResult(
                execution_name=execution.execution_name,
                map_name=execution.map_name,
                particles_count=execution.particles_count,
                total_time=result_data["total_time"],
            )
            self.repo.save_simulation_result(
                execution_name=result.execution_name,
                map_name=result.map_name,
                particles_count=result.particles_count,
                total_time=result.total_time,
            )
            results.append(result)

        return results