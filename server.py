import socket

# Configuração do servidor
host = '0.0.0.0'  # Localhost
port = 12345  # Porta para escutar

# Cria o socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print(f"Servidor aguardando conexões em {host}:{port}...")

# Aceita conexões de clientes
client_socket, client_address = server_socket.accept()
print(f"Conexão estabelecida com {client_address}")

# Recebe a mensagem do cliente
message = client_socket.recv(1024).decode()
print(f"Mensagem recebida do cliente: {message}")

# Responde ao cliente
client_socket.send("Mensagem recebida pelo servidor!".encode())

# Fecha as conexões
client_socket.close()
server_socket.close()
