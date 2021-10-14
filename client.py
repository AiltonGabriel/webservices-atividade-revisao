import socket
import json

SERVER_NAME = '127.0.0.1'
SERVER_PORT = 12000
HEADER_SIZE = 10
BUFFER_SIZE = 64

def main():
    try:
        while True:
            msg = input("Digite a mensagem: ")

            try:
                # Iniciando a conexão com o servidor.
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((SERVER_NAME, SERVER_PORT))

                # Inserindo o cabeçalho com o tamanho da mensagem.
                msg = f"{len(msg):<{HEADER_SIZE}}" + msg
                # Enviando a mensagem para o servidor.
                client_socket.sendall(msg.encode('utf-8'))

                # Obtendo o tamanho da resposta do servidor.
                data = client_socket.recv(BUFFER_SIZE)
                response_len = int(data[:HEADER_SIZE])

                # Recebendo a resposta do servidor.
                response = data[HEADER_SIZE:].decode('utf-8')
                while len(response) < response_len:
                    data = client_socket.recv(BUFFER_SIZE)
                    response += data.decode('utf-8')

                client_socket.close()

                # Transformando a resposta em um dicionário.
                response = json.loads(response)

                # Exibindo os dados da resposta.
                print("\nQuantidade de caracteres da mensagem: {}\n"
                    "Contém números: {}\n"
                    "Quantidade de palavras: {}\n"
                    "Número médio de caracteres das palavras: {}\n"
                    .format(response["n_char"], "Sim" if (response["has_num"]) else "Não", response["n_words"], response["mean_len_words"]))

            except:
                print("\nErro na comunicação com o servidor!\n")
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()