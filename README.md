# Laboratório de Sistemas Distribuídos

Atividades de laboratório da disciplina de Sistemas Distribuídos, em Python.
Cada atividade fica na sua pasta e o repositório evolui commit a commit.

## Estrutura

| Pasta | Tema |
|-------|------|
| `atividade-1/` | Cliente/servidor com sockets (horário e string reversa) |
| `atividade-2/` | RPC com RPyC (horário) |
| `atividade-3/` | Chat em tempo real (sockets + threads) |
| `atividade-4/` | Monitor de Heartbeat |

## Requisitos

- Python 3.9+
- `pip install -r requirements.txt` (só a atividade 2 usa dependência externa)

## Como executar

Cada pasta tem um `README.md` com os comandos. Resumo:

```bash
cd atividade-1 && python servidor_horario.py     # e em outro terminal: python cliente_horario.py
```

## Histórico

O repositório evolui por atividade. Cada uma foi desenvolvida em uma branch
(`atividade-N`), mergeada na `main` e marcada com uma tag (`atividade-N`).
Para ver o código exatamente como estava ao fim de uma atividade:

```bash
git checkout atividade-2
```
