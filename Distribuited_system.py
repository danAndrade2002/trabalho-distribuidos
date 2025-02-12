import threading
import time
import random
from collections import defaultdict
from Process import Process

class DistributedSystem:
    def __init__(self, num_processes,base_port=5000):
        self.processes = {}

        for i in range(num_processes):
            host = "127.0.0.1"  
            port = base_port + i  
            self.processes[i] = Process(i, host, port)

    def connect(self, pid1, pid2):
        self.processes[pid1].add_neighbor(self.processes[pid2])
        self.processes[pid2].add_neighbor(self.processes[pid1])

   
    def start_snapshot(self, initiator):
        print(f"\n=== Iniciando snapshot a partir do processo {initiator} ===\n")
        self.processes[initiator].start_snapshot()

    def simulate_message_passing(self, num_messages=5):
        for _ in range(num_messages):
            p1, p2 = random.sample(list(self.processes.keys()), 2)
            amount = random.randint(10, 100)
            threading.Thread(target=self.processes[p1].transfer_money, args=(p2, amount)).start()
            time.sleep(random.uniform(0.2, 0.6))
