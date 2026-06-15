from aeroSim.simulation.simulation import Simulation
from aeroSim.simulation.batchRunner import BatchSimulationRunner
from aeroSim.graphics.menu import Menu

def main():
    try:
        menu = Menu()

        mode = menu.show_mode()
        if mode == "batch":
            batch_configs = menu.show_batch()
            if not batch_configs:
                return

            runner = BatchSimulationRunner(batch_configs)
            results = runner.run()
            menu.show_batch_results(results)
            return

        # Modo clássico continua com uma única execução.
        particle_count = menu.get_particle_count()
        if particle_count is None:
            return

        selected_map = menu.show()
        if selected_map:
            simulation = Simulation(map_name=selected_map, test_mode=True)
            simulation.run_test(map_name=selected_map, particle_count=particle_count)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()