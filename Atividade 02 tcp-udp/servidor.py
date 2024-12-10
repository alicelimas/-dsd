import socket

# Perguntas do quiz
perguntas = [
    {"pergunta": "Qual país sediou a Copa do Mundo de 2014?", "resposta": "Brasil"},
    {"pergunta": "Qual é o autor de Dom Casmurro?", "resposta": "Machado de Assis"},
    {"pergunta": "Qual cidade é conhecida como A cidade luz?", "resposta": "Paris"},
    {"pergunta": "Qual foi o ano da queda do Muro de Berlim?", "resposta": "1989"},
    {"pergunta": "Em que filme atriz Fernanda Montenegro foi indicada ao Oscar de Melhor Atriz", "resposta": "Central do Brasil"}
]

PORTAS = {
    "TCP": 12345,
    "UDP": 12346
}

def salvar_protocolo(protocolo):
    with open("protocolo.txt", "w") as arquivo:
        arquivo.write(protocolo)

def iniciar_servidor(protocolo):
    salvar_protocolo(protocolo)
    porta = PORTAS[protocolo]
    if protocolo == 'TCP':
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind(('127.0.0.1', porta))
        servidor.listen(1)
        print(f"Servidor TCP aguardando conexão na porta {porta}...")
        conn, addr = servidor.accept()
        print(f"Cliente conectado: {addr}")
        lidar_com_cliente_tcp(conn)
    elif protocolo == 'UDP':
        servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        servidor.bind(('127.0.0.1', porta))
        print(f"Servidor UDP aguardando mensagens na porta {porta}...")
        lidar_com_cliente_udp(servidor)

def lidar_com_cliente_tcp(conn):
    pontuacao = 0
    for pergunta in perguntas:
        conn.send(pergunta["pergunta"].encode())
        resposta = conn.recv(1024).decode().strip()
        if resposta.lower() == "sair":
            break
        if resposta.lower() == pergunta["resposta"].lower():
            pontuacao += 1
            conn.send("Correto!\n".encode())
        else:
            conn.send("Errado.\n".encode())
    conn.send(f"Pontuação final: {pontuacao}/{len(perguntas)}".encode())
    conn.close()

def lidar_com_cliente_udp(servidor):
    pontuacao = 0
    endereco_cliente = None
    for pergunta in perguntas:
        if not endereco_cliente:
            print("Aguardando primeiro contato do cliente...")
            _, endereco_cliente = servidor.recvfrom(1024)
        servidor.sendto(pergunta["pergunta"].encode(), endereco_cliente)
        resposta, endereco_cliente = servidor.recvfrom(1024)
        resposta = resposta.decode().strip()
        if resposta.lower() == "sair":
            break
        if resposta.lower() == pergunta["resposta"].lower():
            pontuacao += 1
            servidor.sendto("Correto!\n".encode(), endereco_cliente)
        else:
            servidor.sendto("Errado.\n".encode(), endereco_cliente)
    servidor.sendto(f"Pontuação final: {pontuacao}/{len(perguntas)}".encode(), endereco_cliente)

if __name__ == "__main__":
    protocolo = input("Escolha o protocolo (TCP/UDP): ").strip().upper()
    if protocolo not in ['TCP', 'UDP']:
        print("Protocolo inválido! Escolha entre TCP ou UDP.")
    else:
        iniciar_servidor(protocolo)
