from Process import Process
from Distribuited_system import DistributedSystem
import time

def main():
    system = DistributedSystem(3)

    
    system.connect(0, 1)
    system.connect(1, 2)
    system.connect(0, 2)

    
    print("\n=== Simulando transações entre processos ===\n")
    system.simulate_message_passing(num_messages=5)

    time.sleep(2)

    print("\n=== Iniciando Snapshot Global ===\n")
    system.start_snapshot(0)

    time.sleep(2)

    print("\n=== Simulação Finalizada ===\n")



if __name__ == "__main__":
    main()