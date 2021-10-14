import socket
import threading
import time
import re
import json

SERVER_PORT = 12000
HEADER_SIZE = 10
BUFFER_SIZE = 64

def connection(connection_socket, addr):
    print("Conexão vinda de {}".format(addr))

    # Obtendo o tamanho da mensagem que será recebida.
    data = connection_socket.recv(BUFFER_SIZE)
    msg_len = int(data[:HEADER_SIZE])

    # Recebendo a mensagem.
    msg = data[HEADER_SIZE:].decode('utf-8')
    while len(msg) < msg_len:
        data = connection_socket.recv(BUFFER_SIZE)
        msg += data.decode('utf-8')

    # Calculando as informações da resoposta.
    response = {}
    response["n_char"] = len(msg)
    response["has_num"] = bool(re.search(r'\d', msg))
    words = msg.split()
    response["n_words"] = len(words)
    response["mean_len_words"] = sum(map(len, words)) / len(words)

    # Transformando a resposta em string.
    response = json.dumps(response)
    response = f"{len(response):<{HEADER_SIZE}}" + response

    # Enviando a resposta para o cliente.
    connection_socket.sendall(response.encode('utf-8'))
    
    connection_socket.close()

def server():
    # Configurando o socket servidor.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', SERVER_PORT))
    server_socket.listen(0)

    while True:
        # Aguandando uma conexão.
        connection_socket, addr =  server_socket.accept()
        # Iniciando uma thread para processar a conexão.
        th = threading.Thread(target=connection, args=(connection_socket, addr))
        th.start()

def main():
    try:
        # Iniciando uma thread deamon para executar o servidor, para que assim seja possível encerrar o programa como CTRL+C.
        th = threading.Thread(target=server)
        th.daemon = True
        th.start()

        # Loop para que a thread principal não encerre, encerrando assim posteriormente a thread deamon do servidor.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()