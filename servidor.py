import socket
import threading

HOST = '192.168.194.25'
PORTA = 50001
special_keys = ["<USERNAME>", "/SAIR"]

users = {}

def enviar_broadcast(mensagem: str, sender):
    for cliente in users.keys():
        if sender and cliente != sender:
            cliente.send(f"\n{mensagem}".encode())

def enviar_unicast(mensagem: str, dest):
    dest.send(f"\n{mensagem}".encode())

def registrar_cliente(conn, addr):
    try:
        dados = conn.recv(1024).decode()
        if dados.endswith(special_keys[0]):
            username = dados.split(special_keys[0])[0]
            users[conn] = username
            enviar_broadcast(f"{users[conn]} entrou para fofocar!", conn)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        conn.close()
        return

def gerenciar_cliente(conn, addr):

    registrar_cliente(conn, addr)

    # Loop para encaminhar mensagens
    while True:
        try:
            dados = conn.recv(1024)
            msg_recebida: str = dados.decode()
            if not dados:
                enviar_broadcast(f"{users[conn]} saiu da fofoca ☹︎", conn)
                break
            if msg_recebida.endswith(special_keys[1]):
                enviar_broadcast(f"{users[conn]} saiu da fofoca ☹︎", conn)
                conn.close()
                del users[conn]

            if "$" in msg_recebida:
                msg_split = msg_recebida.split("$")
                dest = conn
                for cliente in users.keys():
                    if users[cliente] ==  msg_split[0]:
                        dest = cliente
                enviar_unicast(msg_split[1], dest)
                continue

            mensagem = f"\n{users[conn]}> {msg_recebida}"
            enviar_broadcast(mensagem, conn)

        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            break

    conn.close()
    del users[conn]

def iniciar_servidor():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORTA))
    sock.listen()
    print("Servidor em execução, aguardando conexões...")

    while True:
        conn, addr = sock.accept()
        users[conn] = ""
        threading.Thread(target=gerenciar_cliente, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    iniciar_servidor()