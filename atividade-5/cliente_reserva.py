"""Atividade 5 - Cliente RPyC de reserva de assentos.

Uso: python cliente_reserva.py [host] [porta]
"""
import sys

import rpyc

HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORTA = int(sys.argv[2]) if len(sys.argv) > 2 else 18862


def mostrar_mapa(assentos) -> None:
    print("\n=== Mapa de assentos ===")
    for assento, status, dono in assentos:
        if status == "Livre":
            print(f"  {assento:<4} Livre")
        else:
            print(f"  {assento:<4} Reservado ({dono})")
    livres = sum(1 for _, status, _ in assentos if status == "Livre")
    print(f"  -> {livres} livre(s) de {len(assentos)}")


def main() -> None:
    try:
        conn = rpyc.connect(HOST, PORTA)
    except ConnectionRefusedError:
        sys.exit(f"Não foi possível conectar em {HOST}:{PORTA}. O servidor está rodando?")

    nome = input("Seu nome: ").strip()
    try:
        while True:
            mostrar_mapa(conn.root.listar_assentos())
            print("\n[1] Reservar assento   [2] Atualizar mapa   [0] Sair")
            opcao = input("> ").strip()

            if opcao == "1":
                assento = input("Assento (ex: A3): ").strip()
                sucesso, mensagem = conn.root.reservar_assento(nome, assento)
                print(("OK: " if sucesso else "ERRO: ") + mensagem)
            elif opcao == "2":
                continue
            elif opcao == "0":
                break
            else:
                print("Opção inválida.")
    except (KeyboardInterrupt, EOFError):
        print()
    finally:
        conn.close()
        print("Até logo!")


if __name__ == "__main__":
    main()
