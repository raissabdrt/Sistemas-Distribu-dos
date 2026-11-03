# Atividade 2 - RPC com RPyC

Mesma consulta de horário da atividade 1, agora via chamada remota de procedimento.

```bash
pip install -r ../requirements.txt
python servidor_rpc.py     # terminal 1
python cliente_rpc.py      # terminal 2
```

Comparação com a atividade 1: não há `bind/listen/accept/recv`, nem
serialização manual; o método `exposed_obter_horario` é chamado como
`conn.root.obter_horario()`.
