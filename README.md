# projetoPoo2

Simulador de partículas com modo **SANDBOX** e formato de fluxo de ar simples.


## Configuração

As configurações principais estão em `aeroSim/config/simulationConfig.py` e `aeroSim/config/physicsConfig.py`.

- `SIMULATION_MODE`: `"SANDBOX"` ou `"FLUID"`
- `FPS_LIMIT`: limite de frames por segundo
- `GRID_RES`: resolução da malha de fluido (atualmente apenas valores de referência)

## Estrutura

- `aeroSim/main.py` - ponto de entrada do aplicativo
- `aeroSim/simulation/simulation.py` - inicializa loop, tela e mundo
- `aeroSim/core/engine.py` - controle de tempo e eventos do pygame
- `aeroSim/environment/world.py` - definição de mundo, partículas e obstáculos
- `aeroSim/physics/solver.py` - lógica de física e colisões
- `aeroSim/graphics/renderer.py` - desenho de obstáculos e partículas
- `aeroSim/entities/` - modelos de obstáculos e partículas
