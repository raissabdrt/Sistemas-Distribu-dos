# Atividade 5 - Reserva de assentos (estado compartilhado)

Servidor e cliente RPyC. O servidor mantém os assentos A1 a A10 na memória
e todos os clientes enxergam e alteram o mesmo estado.

- **Estado compartilhado:** dicionário no nível do módulo. O `ThreadedServer`
  cria uma instância do serviço por conexão, então atributos de instância
  não seriam compartilhados.
- **Concorrência:** `threading.Lock` em volta de "verificar se está livre +
  reservar", que precisa ser uma operação atômica. Sem isso, dois clientes
  poderiam ler "livre" ao mesmo tempo e ambos receberem sucesso.
- **Métodos expostos:** `exposed_listar_assentos()` e
  `exposed_reservar_assento(nome_cliente, assento)`.

## Executar

```bash
pip install -r ../requirements.txt
python servidor_reserva.py        # terminal 1
python cliente_reserva.py         # terminais 2 e 3 (abra mais de um)
```

No cliente: `1` reserva, `2` atualiza o mapa, `0` sai. Tente reservar o mesmo
assento nos dois clientes: o segundo recebe "Assento X já ocupado".

## Teste automático de concorrência

Com o servidor rodando:

```bash
python teste_concorrencia.py
```

Dispara 20 clientes ao mesmo tempo no mesmo assento (usando `Barrier`) e
verifica que exatamente 1 tem sucesso. Reinicie o servidor para zerar as reservas.
