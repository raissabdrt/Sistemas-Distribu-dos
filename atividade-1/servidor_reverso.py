"""Atividade 1b - Servidor que reverte strings (multithread).

Recebe uma string, devolve ela invertida.
"""
import socket
import threading

HOST = "0.0.0.0"
PORTA = 8000


def atender_cliente(conn: socket.socket, addr) -> None:
    with conn:
        dados = conn.recv(4096)
        if not dados:
            return
        texto = dados.decode("utf-8")
        print(f"[{addr}] recebido: {texto!r}")
        conn.sendall(texto[::-1].encode("utf-8"))


def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORTA))
        servidor.listen()
        print(f"Servidor de string reversa escutando na porta {PORTA}...")
        while True:
            conn, addr = servidor.accept()
            threading.Thread(target=atender_cliente, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
