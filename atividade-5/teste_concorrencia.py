"""Teste de concorrência: N clientes tentam reservar o MESMO assento ao
mesmo tempo. Exatamente um deve ter sucesso; os demais recebem "já ocupado".

Com o servidor rodando: python teste_concorrencia.py
"""
import threading

import rpyc

HOST, PORTA = "127.0.0.1", 18862
CLIENTES = 20
ASSENTOS_TESTE = ["A1", "A5", "A10"]


def tentar(nome, assento, barreira, resultados):
    conn = rpyc.connect(HOST, PORTA)
    try:
        barreira.wait()  # todos disparam juntos
        resultados.append(conn.root.reservar_assento(nome, assento))
    finally:
        conn.close()


def main() -> None:
    falhou = False
    for assento in ASSENTOS_TESTE:
        barreira = threading.Barrier(CLIENTES)
        resultados: list = []
        threads = [
            threading.Thread(target=tentar, args=(f"cliente{i}", assento, barreira, resultados))
            for i in range(CLIENTES)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        sucessos = sum(1 for ok, _ in resultados if ok)
        ocupados = sum(1 for ok, msg in resultados if not ok and "ocupado" in msg)
        status = "PASSOU" if sucessos == 1 and ocupados == CLIENTES - 1 else "FALHOU"
        falhou |= status == "FALHOU"
        print(f"{assento}: {sucessos} sucesso(s), {ocupados} 'já ocupado' de {CLIENTES} -> {status}")

    raise SystemExit(1 if falhou else 0)


if __name__ == "__main__":
    main()
