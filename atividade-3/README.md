# Atividade 3 - Chat em tempo real

Cliente-servidor com sockets TCP e threads.

- **Servidor:** uma thread por cliente; `Lock` protege o dicionário de clientes; broadcast para os demais.
- **Cliente:** uma thread recebe, outra (principal) envia, assim dá para receber enquanto digita.

```bash
python servidor_chat.py            # terminal 1
python cliente_chat.py             # terminais 2, 3, ...
```

Comandos: `/usuarios` lista quem está online, `/sair` desconecta.
Para outra máquina: `python cliente_chat.py <ip-do-servidor> 5000`.
