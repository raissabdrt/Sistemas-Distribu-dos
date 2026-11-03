"""Atividade 3 - Cliente de chat.

Duas threads: uma recebe mensagens do servidor e imprime na tela,
enquanto a thread principal lê o teclado e envia.
Uso: python cliente_chat.py [host] [porta]
"""
import socket
import sys
import threading

HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORTA = int(sys.argv[2]) if len(sys.argv) > 2 else 5000


def receber(sock: socket.socket) -> None:
    arquivo = sock.makefile("r", encoding="utf-8", newline="\n")
    for linha in arquivo:
        print(linha.rstrip("\n"))
    print("Conexão encerrada pelo servidor.")
    # Encerra o input() travado na thread principal
    import os
    os._exit(0)


def main() -> None:
    sock = socket.create_connection((HOST, PORTA))
    threading.Thread(target=receber, args=(sock,), daemon=True).start()
    try:
        while True:
            texto = input()
            sock.sendall((texto + "\n").encode("utf-8"))
            if texto.strip() == "/sair":
                break
    except (KeyboardInterrupt, EOFError):
        try:
            sock.sendall(b"/sair\n")
        except OSError:
            pass
    finally:
        sock.close()


if __name__ == "__main__":
    main()
