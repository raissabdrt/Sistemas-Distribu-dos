"""Atividade 2 - Cliente RPyC: chama obter_horario() remotamente e encerra."""
import rpyc

HOST = "127.0.0.1"
PORTA = 18861

conn = rpyc.connect(HOST, PORTA)
try:
    print(f"Horário do servidor: {conn.root.obter_horario()}")
finally:
    conn.close()
