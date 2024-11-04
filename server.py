import socket
import threading

# Configuração do servidor
host = '0.0.0.0'
port = 65432

# Cria o socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print(f"Servidor aguardando conexões em {host}:{port}...")

clients = []
player_positions = {}
player_lives = {}
enemy_lives = {}
fireballs = []

def handle_client(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(f"Mensagem recebida de {client_address}: {message}")
            if message.startswith("FIREBALL"):
                fireballs.append(message)
                broadcast(message, client_socket)
            elif message.startswith("VIDA"):
                parts = message.split(",")
                if len(parts) == 4:
                    _, x, y, vida = parts
                    player_lives[client_address] = (float(x), float(y), float(vida))
                    broadcast(message, client_socket)
            elif message.startswith("VIDA_INIMIGO"):
                parts = message.split(",")
                if len(parts) == 4:
                    _, x, y, vida = parts
                    enemy_lives[(float(x), float(y))] = float(vida)
                    broadcast(message, client_socket)
            else:
                player_positions[client_address] = message
                broadcast(f"{client_address}:{message}", client_socket)
        except:
            clients.remove(client_socket)
            if client_address in player_positions:
                del player_positions[client_address]
            if client_address in player_lives:
                del player_lives[client_address]
            broadcast(f"REMOVE_PLAYER:{client_address}", client_socket)
            client_socket.close()
            break

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                clients.remove(client)
                client.close()

def send_all_positions(client_socket):
    for address, position in player_positions.items():
        try:
            client_socket.send(f"{address}:{position}".encode())
        except:
            clients.remove(client_socket)
            client_socket.close()

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Conexão estabelecida com {client_address}")
    clients.append(client_socket)
    send_all_positions(client_socket)
    threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
