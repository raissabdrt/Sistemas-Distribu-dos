"""Atividade 1a - Servidor de horário (multithread).

Cada cliente conectado é atendido em uma thread própria: o servidor
envia o horário atual e fecha a conexão.
"""
import socket
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORTA = 8000


def atender_cliente(conn: socket.socket, addr) -> None:
    with conn:
        horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        conn.sendall(horario.encode("utf-8"))
        print(f"[{threading.current_thread().name}] horário enviado para {addr}")


def main() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, PORTA))
        servidor.listen()
        print(f"Servidor de horário escutando na porta {PORTA}...")
        while True:
            conn, addr = servidor.accept()
            threading.Thread(target=atender_cliente, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
