# Atividade 4 - Monitor de Heartbeat

- `worker.py`: envia `PING <ID>` a cada 3 s (UDP).
- `monitor.py`: guarda o último sinal de cada worker; uma thread de checagem
  imprime `[ALERTA] O Nó Worker_X está OFFLINE!` após 8 s sem sinal.

```bash
python monitor.py                  # terminal 1
python worker.py Worker_1          # terminal 2
python worker.py Worker_2          # terminal 3
```

Teste: pare um worker com Ctrl+C e espere ~8 s para ver o alerta.
Se ele voltar, o monitor avisa que está ONLINE de novo.
