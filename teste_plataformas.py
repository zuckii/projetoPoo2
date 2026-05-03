#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de teste para o modo Donkey Kong com plataformas em cascata
"""

from aeroSim.simulation.simulation import Simulation
import time

def main():
    print("=" * 70)
    print("TESTE - PLATAFORMAS DONKEY KONG")
    print("=" * 70)
    print("\nCaracterísticas:")
    print("✓ 9 plataformas em cascata")
    print("✓ Alternância entre horizontal e inclinada (27°)")
    print("✓ Bolinhas caem de uma plataforma para outra")
    print("✓ Responsivo para qualquer resolução")
    print("✓ Sem vazamento lateral")
    print("\nInstruções:")
    print("• ESC ou fechar janela para sair")
    print("• Observe as bolinhas caindo pelas plataformas")
    print("• Cada plataforma tem um padrão específico")
    print("\n" + "=" * 70)
    print("Iniciando simulação...")
    print("=" * 70 + "\n")
    
    try:
        sim = Simulation()
        sim.run()
    except KeyboardInterrupt:
        print("\n\nSimulação interrompida pelo usuário.")
    except Exception as e:
        print(f"\n\nErro durante execução: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
