# Execute a partir da raiz do projeto:
#   uv run python aeroSim\main.py
# ou como pacote:
#   uv run python -m aeroSim.main
# Com uv, o projeto foi executado com sucesso e o build passou sem erro.
# Se não usar uv, também funciona com:
#   python aeroSim\main.py
#   python -m aeroSim.main
import pygame
import sys
import ctypes
from aeroSim.simulation.simulation import Simulation
from aeroSim.persistence.repository import PersistenceRepository

def draw_preview(screen, repo, map_name, rect, w_scale, h_scale):
    ramps = repo.get_maps(map_name)
    for ramp in ramps:
        p1 = (rect.x + int(ramp.x_start * w_scale), rect.y + int(ramp.y_start * h_scale))
        p2 = (rect.x + int(ramp.x_end * w_scale), rect.y + int(ramp.y_end * h_scale))
        pygame.draw.line(screen, (255, 100, 200), p1, p2, 2)

def show_menu():
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        pass

    pygame.init()
    user32 = ctypes.windll.user32
    w = user32.GetSystemMetrics(0)
    h = user32.GetSystemMetrics(1)

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("AeroSim - Selecionar Mapa")
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 24)
    
    repo = PersistenceRepository()
    
    running = True
    selected_map = None
    
    btn_default = pygame.Rect(100, 200, 250, 150)
    btn_funnel = pygame.Rect(450, 200, 250, 150)
    
    w_scale = 250 / w
    h_scale = 150 / h

    while running:
        screen.fill((30, 30, 30))
        
        title = font.render("Selecione o Mapa", True, (255, 255, 255))
        screen.blit(title, (270, 50))
        
        mouse_pos = pygame.mouse.get_pos()
        
        pygame.draw.rect(screen, (60, 60, 80), btn_default)
        pygame.draw.rect(screen, (200, 200, 200), btn_default, 2)
        draw_preview(screen, repo, "default", btn_default, w_scale, h_scale)
        screen.blit(small_font.render("Default", True, (255,255,255)), (110, 210))
        
        pygame.draw.rect(screen, (60, 60, 80), btn_funnel)
        pygame.draw.rect(screen, (200, 200, 200), btn_funnel, 2)
        draw_preview(screen, repo, "funnel", btn_funnel, w_scale, h_scale)
        screen.blit(small_font.render("Funnel", True, (255,255,255)), (460, 210))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_default.collidepoint(mouse_pos):
                    selected_map = "default"
                    running = False
                elif btn_funnel.collidepoint(mouse_pos):
                    selected_map = "funnel"
                    running = False
                    
        pygame.display.flip()
        
    pygame.quit()
    return selected_map

def main():
    map_name = show_menu()
    if map_name:
        simulation = Simulation(map_name=map_name)
        simulation.run()

if __name__ == "__main__":
    main()