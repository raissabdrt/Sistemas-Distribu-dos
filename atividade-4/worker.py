"""Atividade 4 - Worker: envia "PING <id>" ao monitor a cada 3 segundos.

Uso: python worker.py Worker_1 [host] [porta]
Abra vários terminais com IDs diferentes para simular vários nós.
"""
import socket
import sys
import time

INTERVALO = 3  # segundos

if len(sys.argv) < 2:
    sys.exit("Uso: python worker.py <ID_DO_NO> [host] [porta]")

ID_NO = sys.argv[1]
HOST = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1"
PORTA = int(sys.argv[3]) if len(sys.argv) > 3 else 9000

# UDP: um heartbeat é um sinal curto e periódico; perder um datagrama
# não é problema, pois outro chega logo em seguida.
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    print(f"{ID_NO} enviando heartbeat para {HOST}:{PORTA} a cada {INTERVALO}s (Ctrl+C para parar)")
    try:
        while True:
            sock.sendto(f"PING {ID_NO}".encode("utf-8"), (HOST, PORTA))
            time.sleep(INTERVALO)
    except KeyboardInterrupt:
        print(f"\n{ID_NO} encerrado.")
