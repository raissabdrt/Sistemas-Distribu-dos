"""Atividade 3 - Servidor de chat em tempo real.

Arquitetura cliente-servidor com sockets TCP. Cada cliente é atendido
por uma thread; as mensagens são retransmitidas (broadcast) para todos.
Protocolo: texto UTF-8, uma mensagem por linha.
"""
import socket
import threading

HOST = "0.0.0.0"
PORTA = 5000

clientes: dict[socket.socket, str] = {}  # socket -> apelido
trava = threading.Lock()  # protege o dicionário compartilhado entre threads


def enviar(conn: socket.socket, texto: str) -> None:
    try:
        conn.sendall((texto + "\n").encode("utf-8"))
    except OSError:
        pass  # a thread do cliente cuida da remoção


def broadcast(texto: str, remetente: socket.socket | None = None) -> None:
    with trava:
        destinos = [c for c in clientes if c is not remetente]
    for c in destinos:
        enviar(c, texto)


def apelido_em_uso(apelido: str) -> bool:
    with trava:
        return apelido.lower() in (a.lower() for a in clientes.values())


def atender_cliente(conn: socket.socket, addr) -> None:
    arquivo = conn.makefile("r", encoding="utf-8", newline="\n")
    apelido = None
    try:
        enviar(conn, "Bem-vindo ao chat! Digite seu apelido:")
        while True:
            linha = arquivo.readline()
            if not linha:
                return
            apelido = linha.strip()
            if not apelido:
                enviar(conn, "Apelido inválido. Tente de novo:")
            elif apelido_em_uso(apelido):
                enviar(conn, "Apelido já em uso. Tente outro:")
            else:
                break

        with trava:
            clientes[conn] = apelido
        enviar(conn, "Conectado! Comandos: /usuarios, /sair")
        broadcast(f"*** {apelido} entrou no chat ***", conn)
        print(f"[+] {apelido} ({addr[0]}:{addr[1]}) entrou")

        for linha in arquivo:
            msg = linha.strip()
            if not msg:
                continue
            if msg == "/sair":
                break
            if msg == "/usuarios":
                with trava:
                    lista = ", ".join(clientes.values())
                enviar(conn, f"Online: {lista}")
                continue
            broadcast(f"{apelido}: {msg}", conn)
    except (ConnectionError, OSError):
        pass
    finally:
        with trava:
            era_registrado = clientes.pop(conn, None) is not None
        if era_registrado:
            broadcast(f"*** {apelido} saiu do chat ***")
            print(f"[-] {apelido} saiu")
        arquivo.close()
        conn.close()


def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORTA))
        servidor.listen()
        print(f"Servidor de chat escutando na porta {PORTA}...")
        while True:
            conn, addr = servidor.accept()
            threading.Thread(target=atender_cliente, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
