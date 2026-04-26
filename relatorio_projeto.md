### Relatório do Projeto: projetoPoo2

Este é um relatório sobre o projeto **projetopoo2**, um simulador de fluidos aerodinâmicos desenvolvido em Python. O projeto utiliza bibliotecas como Pygame (para gráficos e interface), NumPy e SciPy (para cálculos numéricos), e Pillow (para manipulação de imagens). O objetivo principal é simular comportamentos fluidos, com dois modos principais: **SANDBOX** (simulação baseada em partículas com física simplificada, como gravidade e colisões) e **FLUID** (simulação baseada em grade para fluidos mais avançados).

O projeto é estruturado como um pacote Python (`aeroSim`), com uma arquitetura modular organizada em pastas. Abaixo, descrevo a função de cada pasta com base na análise do código e estrutura do projeto. As descrições são inferidas a partir dos arquivos lidos (como `main.py`, `simulation.py`, configurações e classes principais), nomes dos módulos e dependências.

#### Estrutura Geral do Projeto
- **pyproject.toml**: Arquivo de configuração do projeto (usando setuptools). Define metadados como nome ("projetopoo2"), versão (0.1.0), autor (Zuchi), descrição ("Simulador de Fluidos") e dependências (Pygame, NumPy, SciPy, Pillow). Também configura o build e descoberta de pacotes.
- **README.md**: Documentação básica (atualmente contém apenas o título do projeto).
- **projetopoo2.egg-info/**: Pasta gerada automaticamente pelo setuptools durante o build/install. Contém metadados do pacote (não faz parte do código fonte).
- **aeroSim/**: Pacote principal contendo todos os módulos do simulador.

#### Função de Cada Pasta dentro de `aeroSim/`
1. **analysis/**  
   - **Função**: Destinada à análise e métricas dos resultados da simulação. Por exemplo, poderia calcular estatísticas como velocidade média das partículas, eficiência aerodinâmica ou dados de performance.  
   - **Conteúdo principal**: `metrics.py` (atualmente vazio, indicando que essa funcionalidade ainda não foi implementada).  
   - **Relevância**: Permite avaliar e interpretar os dados gerados pela simulação, útil para estudos científicos ou otimização.

2. **config/**  
   - **Função**: Armazena configurações globais do projeto, separando parâmetros ajustáveis do código principal. Isso facilita a personalização sem modificar o código fonte.  
   - **Conteúdo principal**:  
     - `physicsConfig.py`: Define constantes físicas como densidade do fluido, gravidade, coeficiente de arrasto e parâmetros de partículas (ex.: raio, amortecimento de colisão).  
     - `simulationConfig.py`: Define configurações da simulação, como resolução da grade, limite de FPS e modo (SANDBOX ou FLUID).  
   - **Relevância**: Centraliza ajustes para diferentes cenários de simulação, promovendo reutilização e manutenção.

3. **core/**  
   - **Função**: Contém o núcleo do motor de simulação, responsável pela infraestrutura básica como gerenciamento de tempo, eventos e interface gráfica.  
   - **Conteúdo principal**: `engine.py` (classe `Engine` que inicializa Pygame, controla o loop de tempo, eventos de saída e dimensões da tela).  
   - **Relevância**: É o "coração" do simulador, garantindo que a simulação rode em tempo real com controle de FPS e resposta a entradas do usuário (ex.: fechar com ESC).

4. **entities/**  
   - **Função**: Define as entidades físicas da simulação, como objetos que interagem no ambiente (partículas e obstáculos).  
   - **Conteúdo principal**: Classes para diferentes formas geométricas e partículas:  
     - `particle.py`: Classe `Particle` para objetos móveis com propriedades como posição, velocidade, massa e raio.  
     - Outros: `circle.py`, `obstacle.py`, `polygon.py`, `roof.py`, `wedge.py` (obstáculos estáticos como círculos, polígonos, telhados e cunhas para simular fluxos aerodinâmicos).  
   - **Relevância**: Representa os elementos ativos da simulação, permitindo modelar interações físicas como colisões e movimento.

5. **environment/**  
   - **Função**: Gerencia o ambiente de simulação, incluindo a grade de fluidos, obstáculos e o mundo global onde tudo acontece.  
   - **Conteúdo principal**:  
     - `world.py`: Classe `World` que integra grade, obstáculos e partículas, controlando o spawn automático e atualizações.  
     - `fluidGrid.py`: Provavelmente implementa uma grade para simulações de fluidos (ex.: CFD - Computational Fluid Dynamics).  
     - `obstacleManager.py`: Gerencia a lista de obstáculos no mundo.  
   - **Relevância**: Cria e mantém o "cenário" da simulação, conectando entidades e física para um ambiente coeso.

6. **graphics/**  
   - **Função**: Lida com a renderização visual da simulação, desenhando o mundo na tela usando Pygame.  
   - **Conteúdo principal**: `renderer.py` (classe `Renderer` que configura a tela em fullscreen, desenha obstáculos, partículas e grade, com suporte a fontes para texto).  
   - **Relevância**: Fornece feedback visual em tempo real, essencial para visualizar fluxos aerodinâmicos, colisões e comportamento das partículas.

7. **physics/**  
   - **Função**: Implementa os cálculos físicos e aerodinâmicos, resolvendo equações de movimento e interações.  
   - **Conteúdo principal**:  
     - `solver.py`: Classe `AeroSolver` que executa passos de simulação (ex.: aplicar gravidade, verificar colisões, atualizar posições).  
     - `models/`: Subpasta com modelos de física:  
       - `baseModel.py`: Classe base abstrata para modelos aerodinâmicos.  
       - `simpleModel.py`: Modelo simples que verifica colisões e atualiza posições (usado no modo FLUID).  
   - **Relevância**: O "cérebro" matemático do simulador, aplicando leis físicas como gravidade, arrasto e aerodinâmica para simular comportamentos realistas.

8. **simulation/**  
   - **Função**: Orquestra toda a simulação, integrando engine, mundo, solver e renderer em um loop principal.  
   - **Conteúdo principal**: `simulation.py` (classe `Simulation` que inicializa componentes e roda o loop de atualização/renderização, suportando modos SANDBOX e FLUID).  
   - **Relevância**: É o ponto de entrada lógico, conectando todos os módulos para executar a simulação completa.

#### Como Executar o Projeto
- **Ponto de entrada**: `aeroSim/main.py` (importa e roda `Simulation`).
- **Comandos**: Use `uv run python aeroSim\main.py` ou `python -m aeroSim.main` (requer Python >=3.12).
- **Modos**: 
  - **SANDBOX**: Foco em partículas com física básica (gravidade, vento, colisões).
  - **FLUID**: Usa grade para simulações mais avançadas de fluidos.

#### Observações Finais
- O projeto está em desenvolvimento inicial (versão 0.1.0), com algumas pastas como `analysis` ainda vazias.
- A arquitetura é bem modular, facilitando extensões (ex.: adicionar novos modelos físicos ou entidades).
- Dependências científicas (NumPy, SciPy) sugerem potencial para simulações complexas, mas o código atual foca em física simplificada.
- Para mais detalhes, recomendo revisar os arquivos fonte ou adicionar documentação em `README.md`.

Se precisar de mais detalhes sobre algum módulo específico ou ajuda para expandir o projeto, é só pedir!