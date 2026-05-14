from aeroSim.simulation.simulation import Simulation
from aeroSim.graphics.menu import Menu

def main():
    try:
        menu = Menu()
        map_name = menu.show()
        
        if map_name:
            simulation = Simulation(map_name=map_name)
            simulation.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()