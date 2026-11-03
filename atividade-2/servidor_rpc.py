"""Atividade 2 - Servidor RPC com RPyC.

Evolução da atividade 1: em vez de manipular sockets e bytes na mão,
o cliente chama um método remoto como se fosse uma função local.
"""
from datetime import datetime

import rpyc
from rpyc.utils.server import ThreadedServer

PORTA = 18861


class ServicoHorario(rpyc.Service):
    def on_connect(self, conn):
        print("Cliente conectado.")

    def on_disconnect(self, conn):
        print("Cliente desconectado.")

    def exposed_obter_horario(self) -> str:
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


if __name__ == "__main__":
    servidor = ThreadedServer(ServicoHorario, port=PORTA)
    print(f"Servidor RPyC escutando na porta {PORTA}...")
    try:
        servidor.start()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
