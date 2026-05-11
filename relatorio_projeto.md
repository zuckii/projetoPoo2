### Relatório do Projeto: projetoPoo2

Este é um relatório sobre o projeto **projetopoo2**, um simulador de fluidos aerodinâmicos desenvolvido em Python. O projeto utiliza bibliotecas como Pygame (para gráficos e interface), NumPy e SciPy (para cálculos numéricos), Pillow (para manipulação de imagens) e SQLAlchemy (para persistência de dados em SQLite). O objetivo principal é simular comportamentos fluidos, com dois modos principais: **SANDBOX** (simulação baseada em partículas com física simplificada, como gravidade e colisões) e **FLUID** (simulação baseada em grade para fluidos mais avançados).

O projeto é estruturado como um pacote Python (`aeroSim`), com uma arquitetura modular organizada em pastas, seguindo princípios SOLID (Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion). Abaixo, descrevo a função de cada pasta com base na análise do código e estrutura do projeto. As descrições são inferidas a partir dos arquivos lidos (como `main.py`, `simulation.py`, configurações e classes principais), nomes dos módulos e dependências.

#### Estrutura Geral do Projeto
- **pyproject.toml**: Arquivo de configuração do projeto (usando setuptools). Define metadados como nome ("projetopoo2"), versão (0.1.0), autor (Zuchi), descrição ("Simulador de Fluidos") e dependências (Pygame, NumPy, SciPy, Pillow, SQLAlchemy). Também configura o build e descoberta de pacotes.
- **README.md**: Documentação básica (atualmente contém apenas o título do projeto).
- **relatorio_projeto.md**: Este relatório detalhado sobre a estrutura e funcionalidades.
- **teste_plataformas.py**: Script de teste para plataformas (não integrado ao simulador principal).
- **projetopoo2.egg-info/**: Pasta gerada automaticamente pelo setuptools durante o build/install. Contém metadados do pacote (não faz parte do código fonte).
- **data/**: Pasta criada automaticamente para armazenar o banco de dados SQLite (`sim_data.db`) usado pela camada de persistência.
- **aeroSim/**: Pacote principal contendo todos os módulos do simulador.

#### Função de Cada Pasta dentro de `aeroSim/`
1. **config/**  
   - **Função**: Armazena configurações globais do projeto, separando parâmetros ajustáveis do código principal. Isso facilita a personalização sem modificar o código fonte. Agora unificado em um único arquivo para centralizar todas as constantes.  
   - **Conteúdo principal**:  
     - `settings.py`: Arquivo único com todas as configurações (tamanho de partículas, cores, física, simulação, etc.).  
     - `physicsConfig.py`: Importa constantes físicas de `settings.py` para compatibilidade.  
     - `simulationConfig.py`: Importa configurações de simulação de `settings.py` para compatibilidade.  
   - **Relevância**: Centraliza ajustes para diferentes cenários de simulação, promovendo reutilização e manutenção. Permite alterar facilmente atributos como tamanho e cor das partículas.

2. **core/**  
   - **Função**: Contém o núcleo do motor de simulação, responsável pela infraestrutura básica como gerenciamento de tempo, eventos e interface gráfica.  
   - **Conteúdo principal**: `engine.py` (classe `Engine` que inicializa Pygame, controla o loop de tempo, eventos de saída e dimensões da tela).  
   - **Relevância**: É o "coração" do simulador, garantindo que a simulação rode em tempo real com controle de FPS e resposta a entradas do usuário (ex.: fechar com ESC).

3. **entities/**  
   - **Função**: Define as entidades físicas da simulação, como objetos que interagem no ambiente (partículas e obstáculos). Seguindo princípios SOLID, cada entidade tem responsabilidade única.  
   - **Conteúdo principal**: Classes para diferentes formas geométricas e partículas:  
     - `particle.py`: Classe `Particle` para objetos móveis com propriedades como posição, velocidade, massa, raio e cor (atributos variáveis).  
     - Outros: `circle.py`, `obstacle.py`, `polygon.py`, `roof.py` (obstáculos estáticos como círculos, polígonos e telhados para simular fluxos aerodinâmicos).  
   - **Relevância**: Representa os elementos ativos da simulação, permitindo modelar interações físicas como colisões e movimento. Agora suporta tamanhos e cores ajustáveis para reduzir quantidade de partículas.

4. **environment/**  
   - **Função**: Gerencia o ambiente de simulação, incluindo a grade de fluidos, obstáculos e o mundo global onde tudo acontece. Integrado com persistência para carregar mapas e presets.  
   - **Conteúdo principal**:  
     - `world.py`: Classe `World` que integra grade, obstáculos e partículas, controlando o spawn automático, atualizações e carregamento de mapas/presets.  
     - `fluidGrid.py`: Implementa uma grade para simulações de fluidos (ex.: CFD - Computational Fluid Dynamics).  
   - **Relevância**: Cria e mantém o "cenário" da simulação, conectando entidades e física para um ambiente coeso. Suporta mapas persistidos de rampas.

5. **graphics/**  
   - **Função**: Lida com a renderização visual da simulação, desenhando o mundo na tela usando Pygame.  
   - **Conteúdo principal**: `renderer.py` (classe `Renderer` que configura a tela em fullscreen, desenha obstáculos, partículas (com cores variáveis) e grade, com suporte a fontes para texto).  
   - **Relevância**: Fornece feedback visual em tempo real, essencial para visualizar fluxos aerodinâmicos, colisões e comportamento das partículas.

6. **persistence/**  
   - **Função**: Implementa a camada de persistência usando SQLAlchemy com SQLite local, salvando e carregando mapas de rampas e presets de simulação.  
   - **Conteúdo principal**:  
     - `database.py`: Configura o banco de dados SQLite e sessão SQLAlchemy.  
     - `models.py`: Define modelos ORM para mapas (`MapModel`) e presets (`PresetModel`).  
     - `repository.py`: Classe `PersistenceRepository` para operações CRUD de mapas e presets, com dados padrão automáticos.  
   - **Relevância**: Permite salvar e reutilizar configurações de simulação, atendendo ao requisito de persistência de dados.

7. **physics/**  
   - **Função**: Implementa os cálculos físicos e aerodinâmicos, resolvendo equações de movimento e interações.  
   - **Conteúdo principal**: `solver.py` (classe `AeroSolver` que executa passos de simulação, como aplicar gravidade, verificar colisões e atualizar posições).  
   - **Relevância**: O "cérebro" matemático do simulador, aplicando leis físicas como gravidade, arrasto e aerodinâmica para simular comportamentos realistas.

8. **simulation/**  
   - **Função**: Orquestra toda a simulação, integrando engine, mundo, solver, renderer e persistência em um loop principal.  
   - **Conteúdo principal**: `simulation.py` (classe `Simulation` que inicializa componentes, carrega dados persistidos e roda o loop de atualização/renderização, suportando modos SANDBOX e FLUID).  
   - **Relevância**: É o ponto de entrada lógico, conectando todos os módulos para executar a simulação completa.

#### Como Executar o Projeto
- **Ponto de entrada**: `aeroSim/main.py` (importa e roda `Simulation`).
- **Comandos**: Use `uv run python aeroSim\main.py` ou `python -m aeroSim.main` (requer Python >=3.12).
- **Modos**: 
  - **SANDBOX**: Foco em partículas com física básica (gravidade, vento, colisões), agora com atributos variáveis (tamanho e cor) e mapas persistidos.
  - **FLUID**: Usa grade para simulações mais avançadas de fluidos.
- **Persistência**: O projeto cria automaticamente um banco SQLite em `data/sim_data.db` com mapas padrão (ex.: 3 rampas) e presets iniciais. Mapas e presets podem ser salvos/carregados via `PersistenceRepository`.
- **Configurações**: Ajuste variáveis em `aeroSim/config/settings.py` para personalizar (ex.: `PARTICLE_RADIUS`, `PARTICLE_MAX_COUNT`, cores, etc.).

#### Observações Finais
- O projeto foi refatorado seguindo princípios SOLID, com separação clara de responsabilidades (entidades, física, renderização, persistência).
- Implementada persistência de dados com SQLAlchemy e SQLite para mapas de rampas e presets de simulação, atendendo aos requisitos do professor.
- Partículas agora suportam atributos variáveis (tamanho e cor), permitindo reduzir a quantidade de spawn para otimização.
- A arquitetura modular facilita extensões (ex.: adicionar novos modelos físicos ou entidades).
- Dependências científicas (NumPy, SciPy) sugerem potencial para simulações complexas, mas o código atual foca em física simplificada com foco em POO.
- Para mais detalhes, recomendo revisar os arquivos fonte ou adicionar documentação em `README.md`.
