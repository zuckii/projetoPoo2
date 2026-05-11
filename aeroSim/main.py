from aeroSim.simulation.simulation import Simulation
from aeroSim.graphics.menu import Menu

def main():
    menu = Menu()
    map_name = menu.show()
    
    if map_name:
        simulation = Simulation(map_name=map_name)
        simulation.run()

if __name__ == "__main__":
    main()