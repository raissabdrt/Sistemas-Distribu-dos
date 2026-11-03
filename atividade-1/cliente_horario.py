"""Atividade 1a - Cliente de horário: pede o horário ao servidor e encerra."""
import socket

HOST = "127.0.0.1"
PORTA = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORTA))
    horario = s.recv(1024).decode("utf-8")
    print(f"Horário do servidor: {horario}")
