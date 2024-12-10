import socket

PORTAS = {
    "TCP": 12345,
    "UDP": 12346
}

def ler_protocolo():
    try:
        with open("protocolo.txt", "r") as arquivo:
            return arquivo.read().strip()
    except FileNotFoundError:
        print("Erro: O servidor ainda não foi iniciado ou o protocolo não foi definido.")
        exit()

def iniciar_cliente(protocolo):
    porta = PORTAS[protocolo]
    if protocolo == 'TCP':
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(('127.0.0.1', porta))
        comunicar_tcp(cliente)
    elif protocolo == 'UDP':
        cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        endereco_servidor = ('127.0.0.1', porta)
        cliente.sendto("Início da comunicação".encode(), endereco_servidor)  # Inicializa a comunicação
        comunicar_udp(cliente, endereco_servidor)

def comunicar_tcp(cliente):
    while True:
        pergunta = cliente.recv(1024).decode()
        if "Pontuação final" in pergunta:
            print(pergunta)
            break
        print("Pergunta:", pergunta)
        resposta = input("Resposta: ")
        cliente.send(resposta.encode())
        if resposta.lower() == "sair":
            pontuacao = cliente.recv(1024).decode()  # Recebe a pontuação final
            print(pontuacao)
            break
        feedback = cliente.recv(1024).decode()
        print(feedback)
    cliente.close()

def comunicar_udp(cliente, endereco_servidor):
    while True:
        pergunta, _ = cliente.recvfrom(1024)
        if "Pontuação final" in pergunta.decode():
            print(pergunta.decode())
            break
        print("Pergunta:", pergunta.decode())
        resposta = input("Resposta: ")
        cliente.sendto(resposta.encode(), endereco_servidor)
        if resposta.lower() == "sair":
            pontuacao = cliente.recv(1024).decode()  # Recebe a pontuação final
            print(pontuacao)
            break
        feedback, _ = cliente.recvfrom(1024)
        print(feedback.decode())
    cliente.close()

if __name__ == "__main__":
    protocolo = ler_protocolo()
    print(f"Protocolo definido pelo servidor: {protocolo}")
    iniciar_cliente(protocolo)
