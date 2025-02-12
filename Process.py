import socket
import threading
import random
import time
from collections import defaultdict

class Process:
    def __init__(self, pid, host, port):
        self.pid = pid
        self.host = host
        self.port = port
        self.neighbors = {}
        self.balance = random.randint(1000, 5000) 
        self.transactions = []  
        self.recording = False
        self.snapshots = {}
        self.channels = defaultdict(list)
        print(f"Processo {self.pid} Balance {self.balance}")
        self.server_thread = threading.Thread(target=self.start_server, daemon=True)
        self.server_thread.start()

        

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()
        print(f"Processo {self.pid} ouvindo em {self.host}:{self.port}...")

        while True:
            conn, addr = server.accept()
            threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()


    def add_neighbor(self, neighbor):
        self.neighbors[neighbor.pid] = (neighbor.host, neighbor.port)
    
    def handle_client(self, conn):
        message = conn.recv(1024).decode()
        if message.startswith("TRANSFER"):
            self.handle_transaction(message)
        elif message == "MARKER":
            self.handle_marker()
        else:
            print(f"Process {self.pid} recebeu mensagem desconhecida: {message}")

    def send_message(self, neighbor, message):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(neighbor)
            client.send(message.encode())
            client.close()
        except ConnectionRefusedError:
            print(f"Process {self.pid}: Falha ao conectar a {neighbor}")

    def handle_transaction(self, message):
        _, sender, amount = message.split()
        sender = int(sender)
        amount = int(amount)
        self.balance += amount
        self.transactions.append((sender, self.pid, amount))
        print(f"Process {self.pid} recebeu transferência de {amount} de Process {sender}. Saldo atual: {self.balance}")

    def transfer_money(self, to_pid, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.transactions.append((self.pid, to_pid, amount))
            print(f"Process {self.pid} enviando {amount} para Process {to_pid}. Saldo restante: {self.balance}")
            self.send_message(self.neighbors[to_pid], f"TRANSFER {self.pid} {amount}")
        else:
            print(f"Process {self.pid} tentou transferir {amount}, mas saldo insuficiente!")

    def handle_marker(self):
        if not self.recording:
            self.recording = True
            self.snapshots['balance'] = self.balance
            self.snapshots['transactions'] = list(self.transactions)
            print(f"Process {self.pid} registrou snapshot: Saldo {self.balance}, Transações {self.transactions}")
            for neighbor in self.neighbors.values():
                self.send_message(neighbor, "MARKER")

    def start_snapshot(self):
        print(f"Process {self.pid} iniciando snapshot...")
        self.recording = True
        self.snapshots['balance'] = self.balance
        self.snapshots['transactions'] = list(self.transactions)
        for neighbor in self.neighbors.values():
            self.send_message(neighbor, "MARKER")
