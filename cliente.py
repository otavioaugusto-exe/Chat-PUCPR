import socket
import threading

HOST = '192.168.194.25'
PORTA = 50001
special_keys = ["<USERNAME>"]
username = ""
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORTA))

def receber_mensagens():
    while True:
        try:
            dados = sock.recv(1024)
            if not dados:
                print("Servidor desconectado.")
                break
            print(dados.decode())
        except Exception as e:
            print(f"Ocorreu um erro ao receber a mensagem: {e}")
            break

def get_username():
    global username
    while True:
        username = input("Digite um usuário para se registrar: ")
        if username != "":
            sock.sendall(f"{username}{special_keys[0]}".encode())
            break

threading.Thread(target=receber_mensagens).start()
get_username()
while True:
    mensagem = input(f"{username}> ")
    if "/SAIR" in mensagem:
        sock.sendall(mensagem.encode())
        break
    sock.sendall(mensagem.encode())
