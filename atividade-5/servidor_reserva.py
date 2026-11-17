"""Atividade 5 - Servidor RPyC de reserva de assentos (estado compartilhado).

O ThreadedServer cria UMA instância do serviço por conexão, então o estado
não pode ficar em atributos de instância: ele vive no nível do módulo e é
compartilhado por todas as conexões (threads). Como várias threads mexem
nele ao mesmo tempo, toda leitura/escrita passa por um Lock.
"""
import threading

import rpyc
from rpyc.utils.server import ThreadedServer

PORTA = 18862
ASSENTOS = [f"A{i}" for i in range(1, 11)]  # A1 ... A10

# Estado compartilhado: assento -> nome de quem reservou (None = livre)
_reservas: dict[str, str | None] = {a: None for a in ASSENTOS}
_trava = threading.Lock()


class ServicoReserva(rpyc.Service):
    def on_connect(self, conn):
        print("[+] cliente conectado")

    def on_disconnect(self, conn):
        print("[-] cliente desconectado")

    def exposed_listar_assentos(self):
        """Retorna uma tupla de (assento, status, reservado_por).

        Tuplas de strings são enviadas por valor pelo RPyC (um dict ou list
        voltaria como proxy de objeto remoto).
        """
        with _trava:
            return tuple(
                (a, "Livre" if dono is None else "Reservado", dono or "")
                for a, dono in _reservas.items()
            )

    def exposed_reservar_assento(self, nome_cliente, assento):
        """Tenta reservar. Retorna (sucesso: bool, mensagem: str)."""
        nome = str(nome_cliente).strip()
        codigo = str(assento).strip().upper()

        if not nome:
            return (False, "Informe o nome do cliente.")
        if codigo not in _reservas:
            return (False, f"Assento {codigo!r} não existe (use A1 a A10).")

        # Seção crítica: verificar e reservar precisam ser UMA operação
        # atômica. Sem o Lock, duas threads poderiam ver "livre" ao mesmo
        # tempo e as duas confirmariam a reserva (condição de corrida).
        with _trava:
            if _reservas[codigo] is not None:
                resultado = (False, f"Assento {codigo} já ocupado.")
            else:
                _reservas[codigo] = nome
                resultado = (True, f"Assento {codigo} reservado para {nome}.")

        print(f"[reserva] {nome} -> {codigo}: {resultado[1]}")
        return resultado


if __name__ == "__main__":
    servidor = ThreadedServer(ServicoReserva, port=PORTA)
    print(f"Servidor de reservas escutando na porta {PORTA} ({len(ASSENTOS)} assentos)...")
    try:
        servidor.start()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
