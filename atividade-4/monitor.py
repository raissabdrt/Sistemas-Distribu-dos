"""Atividade 4 - Servidor Monitor de Heartbeat.

- Thread principal: recebe os "PING <id>" e registra o instante do último sinal.
- Thread de checagem: a cada segundo, marca como OFFLINE quem passou
  de 8 segundos sem enviar heartbeat.
"""
import socket
import threading
import time

HOST = "0.0.0.0"
PORTA = 9000
TIMEOUT = 8          # segundos sem sinal => OFFLINE
INTERVALO_CHECAGEM = 1

ultimo_sinal: dict[str, float] = {}   # id -> time.monotonic() do último PING
offline: set[str] = set()             # nós já alertados (evita alerta repetido)
trava = threading.Lock()


def checar_workers() -> None:
    while True:
        time.sleep(INTERVALO_CHECAGEM)
        agora = time.monotonic()
        with trava:
            for no, instante in ultimo_sinal.items():
                if agora - instante > TIMEOUT and no not in offline:
                    offline.add(no)
                    print(f"[ALERTA] O Nó {no} está OFFLINE!")


def main() -> None:
    threading.Thread(target=checar_workers, daemon=True).start()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, PORTA))
        print(f"Monitor escutando na porta {PORTA} (timeout: {TIMEOUT}s)...")
        while True:
            dados, addr = sock.recvfrom(1024)
            partes = dados.decode("utf-8", errors="replace").split()
            if len(partes) != 2 or partes[0] != "PING":
                continue  # ignora mensagens fora do protocolo
            no = partes[1]
            with trava:
                novo = no not in ultimo_sinal
                voltou = no in offline
                ultimo_sinal[no] = time.monotonic()
                offline.discard(no)
            if novo:
                print(f"[INFO] Nó {no} registrado ({addr[0]})")
            elif voltou:
                print(f"[INFO] Nó {no} voltou a ficar ONLINE")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nMonitor encerrado.")
