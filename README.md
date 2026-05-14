# AeroSim - Particle Physics Simulator

Este é um projeto de Programação Orientada a Objetos 2 (POO2) que demonstra conceitos avançados de engenharia de software, incluindo **Reusabilidade de Software**, **Padrões de Projeto** e **Frameworks**.

## Visão Geral do Projeto

AeroSim é um simulador de física de partículas 2D construído com Pygame e SQLAlchemy. Simula partículas caindo sob gravidade, quicando em obstáculos e interagindo entre si. A arquitetura segue um design modular com separação clara de responsabilidades entre física, renderização, persistência e gerenciamento de entidades.

**Tecnologias Utilizadas:**
- **Framework:** Pygame 2.6.1 (renderização e tratamento de eventos)
- **Banco de Dados:** SQLAlchemy 2.0.49 com SQLite (persistência de mapas e predefinições)
- **Linguagem:** Python 3.12+
- **Padrão Arquitetural:** Arquitetura em camadas com design orientado a domínio

**Tópicos de POO2 Demonstrados:**
- **Reusabilidade de Software:** Componentes modulares como Particle, Obstacle, AeroSolver podem ser reutilizados em outros simuladores
- **Padrões de Projeto:** Strategy (colisões polimórficas), Repository (abstração de dados), Coordinator (orquestração), Façade (inicialização), Observer (atualizações baseadas em tempo)
- **Frameworks:** Uso de Pygame como framework de jogos e SQLAlchemy como ORM

## Estrutura do Projeto

```
pyproject.toml
README.md
aeroSim/
	__init__.py
	main.py
	config/
		__init__.py
		physicsConfig.py
		settings.py
		simulationConfig.py
	core/
		__init__.py
		engine.py
	entities/
		__init__.py
		obstacle.py
		particle.py
		polygon.py
		roof.py
	environment/
		__init__.py
		world.py
	graphics/
		__init__.py
		menu.py
		renderer.py
	persistence/
		__init__.py
		models.py
		repository.py
	physics/
		__init__.py
		solver.py
	simulation/
		__init__.py
		simulation.py
data/
projetopoo2.egg-info/
	dependency_links.txt
	PKG-INFO
	requires.txt
	SOURCES.txt
	top_level.txt
```

## Descrição dos Arquivos e Pastas

### **1. Core Package (`aeroSim/`)**

#### **Entry Point: [`main.py`](aeroSim/main.py)**
- **Função:** Ponto de entrada da aplicação que orquestra a sequência de inicialização
- **Padrões:** Façade pattern - abstrai complexidade de inicialização
- **Interação:** Menu → Simulação

#### **Core Engine: [`core/engine.py`](aeroSim/core/engine.py)**
- **Classe:** `Engine`
- **Função:** Gerencia relógio da aplicação, limitação de taxa de quadros e polling de eventos
- **Padrões:** Singleton-like para controle do loop principal
- **Reusabilidade:** Pode ser extraído para um módulo de engine gráfico separado

### **2. Simulation Module (`aeroSim/simulation/`)**

#### **Simulation Orchestrator: [`simulation.py`](aeroSim/simulation/simulation.py)**
- **Classe:** `Simulation`
- **Função:** Coordenador central que conecta todos os subsistemas
- **Fluxo Arquitetural:**
  ```
  Engine.update_time(dt)
    ↓
  Solver.step_sandbox(world, dt)
    ↓
  World.update(dt)
    ↓
  Renderer.render(world)
  ```
- **Padrões:** Coordinator/Orchestrator pattern

### **3. Configuration Module (`aeroSim/config/`)**

#### **Physics Settings: [`physicsConfig.py`](aeroSim/config/physicsConfig.py)**
- **Função:** Re-exporta constantes físicas de settings
- **Uso:** AeroSolver para comportamento de partículas

#### **Simulation Settings: [`simulationConfig.py`](aeroSim/config/simulationConfig.py)**
- **Constantes:** FPS_LIMIT, SIMULATION_MODE

#### **Main Settings File: [`settings.py`](aeroSim/config/settings.py)**
- **Parâmetros Físicos:** GRAVITY, BOUNCE_DAMPING, PARTICLE_RADIUS, etc.
- **Padrões:** Configuration as code (fonte única de verdade)

### **4. Entities Module (`aeroSim/entities/`)**

#### **Base Class: [`obstacle.py`](aeroSim/entities/obstacle.py)**
- **Classe:** `Obstacle` (Abstract Base Class)
- **Função:** Interface para todos os objetos colidíveis
- **Padrões:** Strategy pattern para tratamento polimórfico de colisões

#### **Particle Entity: [`particle.py`](aeroSim/entities/particle.py)**
- **Classe:** `Particle`
- **Atributos:** Posição, velocidade, massa, raio, cor, estado
- **Métodos:** update_position, apply_acceleration, bounce
- **Reusabilidade:** Classe genérica de partícula; pode ser estendida

#### **Polygon Obstacle: [`polygon.py`](aeroSim/entities/polygon.py)**
- **Classe:** `Polygon(Obstacle)`
- **Função:** Retângulos AABB para obstáculos estáticos
- **Uso:** Paredes da tela

#### **Roof Obstacle: [`roof.py`](aeroSim/entities/roof.py)**
- **Classe:** `Roof(Obstacle)`
- **Função:** Segmentos de linha que podem rotacionar
- **Uso:** Rampas e plataformas

### **5. Physics Module (`aeroSim/physics/`)**

#### **Physics Solver: [`solver.py`](aeroSim/physics/solver.py)**
- **Classe:** `AeroSolver`
- **Função:** Todos os cálculos físicos e resolução de colisões
- **Método:** Sub-stepping (4 iterações por quadro)
- **Padrões:** Strategy pattern para tipos diferentes de obstáculos

### **6. Environment Module (`aeroSim/environment/`)**

#### **World State: [`world.py`](aeroSim/environment/world.py)**
- **Classe:** `World`
- **Função:** Container para todas as entidades da simulação
- **Padrões:** Repository pattern para carregamento de mapas

### **7. Graphics Module (`aeroSim/graphics/`)**

#### **Menu System: [`menu.py`](aeroSim/graphics/menu.py)**
- **Classe:** `Menu`
- **Função:** Interface interativa de seleção de mapas
- **Padrões:** Observer pattern para tratamento de entrada

#### **Renderer: [`renderer.py`](aeroSim/graphics/renderer.py)**
- **Classe:** `Renderer`
- **Função:** Todas as operações de desenho

### **8. Persistence Module (`aeroSim/persistence/`)**

#### **Data Models: [`models.py`](aeroSim/persistence/models.py)**
- **Modelos:** MapModel, PresetModel

#### **Repository: [`repository.py`](aeroSim/persistence/repository.py)**
- **Classe:** `PersistenceRepository`
- **Função:** Camada ORM SQLAlchemy para acesso ao banco
- **Padrões:** Repository pattern

### **9. Data Storage (`data/`)**

- **`sim_data.db`**: Banco SQLite com mapas e predefinições

### **Outros Arquivos**
- **`pyproject.toml`**: Configuração do projeto Python
- **`projetopoo2.egg-info/`**: Metadados do pacote

## Funcionalidades

- Geração de partículas com tamanhos e cores aleatórios
- Física de gravidade e colisões
- Múltiplos tipos de obstáculos (paredes, rampas)
- Menu de seleção de mapas
- Display em tela cheia

## Instalação

1. Instalar Python 3.12+
2. Instalar dependências: `pip install pygame sqlalchemy`
3. Executar: `python -m aeroSim.main`

## Configuração

Editar `aeroSim/config/settings.py` para ajustar:
- FPS_LIMIT: Taxa de quadros alvo
- GRAVITY: Aceleração descendente (pixels/s²)
- WIND_X/WIND_Y: Forças do vento
- DRAG_COEFFICIENT: Resistência do ar
- BOUNCE_DAMPING: Perda de energia em quiques
- PARTICLE_RADIUS: Tamanho padrão da partícula

## Mapas

Mapas armazenados em banco SQLite (`data/sim_data.db`):
- default: Rampas básicas
- funnel: Estrutura complexa de funil
- dk2: Plataformas inspiradas em Donkey Kong

## Controles

- ESC: Sair da simulação
- Mouse: Selecionar mapa no menu
