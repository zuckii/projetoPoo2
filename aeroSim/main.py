# Execute a partir da raiz do projeto:
#   uv run python aeroSim\main.py
# ou como pacote:
#   uv run python -m aeroSim.main
# Com uv, o projeto foi executado com sucesso e o build passou sem erro.
# Se não usar uv, também funciona com:
#   python aeroSim\main.py
#   python -m aeroSim.main
from aeroSim.simulation.simulation import Simulation


def main() -> None:
    simulation = Simulation()
    simulation.run()


if __name__ == "__main__":
    main()