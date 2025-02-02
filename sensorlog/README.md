# Documentação das Classes do Diretório sensorlog

Este documento fornece uma visão geral e detalhada sobre as classes presentes no diretório sensorlog. O objetivo é auxiliar os desenvolvedores no entendimento e utilização dessas classes.

---

## Classe: `Id`

### Descrição
A classe `Id` é uma classe base projetada para armazenar informações comuns relacionadas a identificadores e meta-informações, como horário, canal e dispositivos.

### Construtor
```python
Id(
    time: Optional[datetime | int] = datetime.now(),
    timezone_offset: Optional[timedelta | int] = timedelta(hours=0),
    channel_id: Optional[int] = None,
    channel_name: Optional[str] = None,
    message_id: Optional[int] = None,
    bot_id: Optional[int] = None,
    bot_name: Optional[str] = None,
    device_id: Optional[int] = None,
    device_name: Optional[str] = None,
)
```

### Atributos
- `time`: Instante do evento (datetime ou timestamp).
- `timezone_offset`: Diferença de fuso horário (timedelta ou segundos).
- `channel_id`: ID do canal associado.
- `channel_name`: Nome do canal associado.
- `message_id`: ID da mensagem associada.
- `bot_id`: ID do bot.
- `bot_name`: Nome do bot.
- `device_id`: ID do dispositivo.
- `device_name`: Nome do dispositivo.

### Métodos
- Propriedades com getters e setters para `time` e `timezone_offset`.
- `__str__()`: Retorna uma representação textual dos atributos.

---

## Classe: `Events`

### Descrição
Herdando de `Id`, a classe `Events` é projetada para representar eventos associados a dispositivos ou sistemas.

### Construtor
```python
Events(
    event_type: int,
    event_text: str,
    event_flag: str = "",
    **kwargs
)
```

### Atributos
- `type`: Tipo do evento (inteiro).
- `flag`: Indicador do evento (string).
- `text`: Texto descritivo do evento.

### Métodos
- `__str__()`: Inclui informações adicionais sobre o evento, além das propriedades herdadas.

---

## Classe: `Values`

### Descrição
Herdando de `Id`, a classe `Values` é destinada a armazenar e manipular dados de sensores e suas respectivas medições.

### Construtor
```python
Values(**kwargs)
```

### Atributos
- `level`, `raw_level`, `distance`, `t0`, `t1`, `v0`, `v1`: Dados de sensores (float).
- `snr`, `rssi`, `snr_gw`, `rssi_gw`, `speed1`, `speed2`: Métricas do sistema (int).

### Métodos
- `__str__()`: Retorna uma representação detalhada das medições e atributos.

---

## Classe: `SetValues`

### Descrição
Herdando de `Values`, a classe `SetValues` introduz um mecanismo de tradução e configuração de valores com base em chaves de texto.

### Construtor
```python
SetValues(**kwargs)
```

### Atributos Privados
- `__translate`: Dicionário de tradução de chaves para atributos internos.

### Métodos
- `set_value(key, value)`: Traduz e define o valor do atributo correspondente.

---

## Classe: `Decode`

### Descrição
Responsável por interpretar mensagens recebidas e convertê-las em instâncias das classes `SetValues` ou `Events`.

### Construtor
```python
Decode(m: types.Message)
```

### Atributos
- `var_data`: Armazena a instância de `SetValues` ou `Events` criada a partir da mensagem.

### Lógica de Funcionamento
1. Divide o texto da mensagem em linhas.
2. Analisa e extrai o nome do dispositivo e seus valores.
3. Identifica e classifica eventos com base em padrões predefinidos.

---

### Considerações Finais
Essas classes são projetadas para integrar dados de sensores e eventos com sistemas de mensagens. Certifique-se de inicializar os objetos com os dados corretos para garantir a funcionalidade esperada.

Documentação criada para facilitar a compreensão e uso das classes no diretório sensorlog.

