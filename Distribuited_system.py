import threading
import time
import random
from collections import defaultdict
from Process import Process

class DistributedSystem:
    def __init__(self, num_processes):
        self.processes = {i: Process(i, self) for i in range(num_processes)}
        self.connections = defaultdict(list)

    def connect(self, p1, p2):
        """Cria uma conexão bidirecional entre dois processos."""
        self.connections[p1].append(p2)
        self.connections[p2].append(p1)
    
    def get_neighbors(self, pid):
        return self.connections[pid]

    def start_snapshot(self, initiator):
        """Inicia o algoritmo de Chandy-Lamport a partir de um processo específico."""
        threading.Thread(target=self.processes[initiator].start_snapshot).start()
    
    def simulate_message_passing(self, num_messages=5):
        """Simula a troca de mensagens entre processos."""
        for _ in range(num_messages):
            p1, p2 = random.sample(list(self.processes.keys()), 2)
            threading.Thread(target=self.processes[p1].send_message, args=(p2, f"MSG_{p1}->{p2}")).start()
            time.sleep(random.uniform(0.2, 0.6))
