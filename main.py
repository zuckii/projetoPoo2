import pygame
import numpy as np

# 1. Configurações da Janela e Grade
WIDTH, HEIGHT = 500, 500
GRID_SIZE = 100  # Uma grade de 100x100 células
CELL_SIZE = WIDTH // GRID_SIZE

# Inicializa o Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Fluidos - Protótipo")
clock = pygame.time.Clock()

# 2. A Estrutura de Dados (POO Básica)
class FluidGrid:
    def __init__(self, size):
        self.size = size
        # Array do NumPy que guarda a quantidade de "tinta" em cada célula
        self.density = np.zeros((size, size))

    def add_density(self, x, y, amount):
        # Converte a coordenada do mouse para a coordenada da grade
        grid_x = int(x / CELL_SIZE)
        grid_y = int(y / CELL_SIZE)
        
        # Garante que o clique não dê erro fora da tela
        if 0 <= grid_x < self.size and 0 <= grid_y < self.size:
            self.density[grid_x, grid_y] += amount
            # Limita o valor máximo para renderizar a cor corretamente (0 a 255)
            self.density[grid_x, grid_y] = min(self.density[grid_x, grid_y], 255)

    def update_physics(self):
        # Física Básica: Decaimento. Multiplica por 0.95 para a tinta ir sumindo.
        # Nas próximas etapas, substituiremos isso pela matemática real dos fluidos.
        self.density *= 0.95

# Instancia a nossa grade
fluid = FluidGrid(GRID_SIZE)

# 3. Loop Principal do Motor
running = True
while running:
    # Checa se o usuário fechou a janela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Interação: Se clicar ou segurar o botão esquerdo, adiciona fluido
    mouse_buttons = pygame.mouse.get_pressed()
    if mouse_buttons[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        fluid.add_density(mouse_x, mouse_y, 200) # Injeta densidade

    # Atualiza a física do quadro atual
    fluid.update_physics()

    # 4. Renderização (Desenho na tela)
    screen.fill((0, 0, 0)) # Fundo limpo (preto)
    
    # Varre a grade e pinta os quadrados que têm fluido
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            d = fluid.density[i, j]
            if d > 5: # Só desenha se houver densidade visível para economizar CPU
                # Cria uma cor estilo "Neon" (Azul para Roxo)
                color = (int(d * 0.4), int(d * 0.1), int(d)) 
                pygame.draw.rect(screen, color, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Atualiza a tela
    pygame.display.flip()
    # Crava em 60 Frames por Segundo
    clock.tick(60)

pygame.quit()