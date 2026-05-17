from aeroSim.simulation.simulation import Simulation
from aeroSim.graphics.menu import Menu

def main():
    try:
        menu = Menu()
        
        # Primeiro, usuário escolhe número de partículas
        particle_count = menu.get_particle_count()
        if particle_count is None:
            return
        
        # Depois escolhe o mapa
        selected_map = menu.show()
        if selected_map:
            # Todos os mapas executam como teste
            simulation = Simulation(map_name=selected_map, test_mode=True)
            simulation.run_test(map_name=selected_map, particle_count=particle_count)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()