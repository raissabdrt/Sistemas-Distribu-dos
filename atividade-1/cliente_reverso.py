"""Atividade 1b - Cliente: envia uma string e imprime a resposta revertida."""
import socket

HOST = "127.0.0.1"
PORTA = 8000
MENSAGEM = "Olá, Mundo Distribuído"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORTA))
    s.sendall(MENSAGEM.encode("utf-8"))
    resposta = s.recv(4096).decode("utf-8")
    print(f"Enviado:  {MENSAGEM}")
    print(f"Recebido: {resposta}")
