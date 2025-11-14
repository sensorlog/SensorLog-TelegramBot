# Documentação do pacote `sensorlog`

As classes deste diretório compõem o núcleo reutilizável do SensorLog-TelegramBot. Elas abstraem os metadados das mensagens recebidas do Telegram, centralizam a normalização de valores e expõem estruturas prontas para serialização ou armazenamento.

## Visão geral
| Componente | Finalidade |
| --- | --- |
| `Id` | Guarda metadados compartilhados (horário, canal, bot, dispositivo). |
| `Values` | Representa medições periódicas dos sensores. |
| `SetValues` | Extensão de `Values` que traduz pares texto → atributo. |
| `Events` | Representa alertas e notificações de dispositivos. |
| `Decode` | Converte `types.Message` do TeleBot em `Values` ou `Events`. |

---

## Classe `Id`
`Id` encapsula os atributos comuns a qualquer mensagem recebida.

```python
Id(
    time: datetime | int | None = None,
    timezone_offset: timedelta | int | None = timedelta(),
    channel_id: int | None = None,
    channel_name: str | None = None,
    message_id: int | None = None,
    bot_id: int | None = None,
    bot_name: str | None = None,
    device_id: int | None = None,
    device_name: str | None = None,
)
```

- `time` aceita `datetime` ou timestamp; valores `None` são convertidos para `datetime.now()`.
- `timezone_offset` suporta `timedelta` ou segundos inteiros.
- Os demais campos são preenchidos de acordo com o conteúdo do canal do Telegram.

---

## Classe `Values`
Herda de `Id` e possui slots para todas as medições disponibilizadas pelos sensores:

- `level`, `raw_level`, `distance`
- `t0`, `t1`, `v0`, `v1`
- `snr`, `rssi`, `snr_gw`, `rssi_gw`
- `speed1`, `speed2`, `counter`, `digital_input`

A representação textual (`__str__`) lista tanto os metadados quanto as leituras, facilitando logs.

---

## Classe `SetValues`
Subclasse de `Values` que disponibiliza o método `set_value(key, value)`. Ele utiliza um dicionário privado de tradução (`__TRANSLATE`) para mapear as chaves humanizadas presentes nas mensagens do Telegram para os atributos internos. Conversões numéricas são aplicadas automaticamente (`_float`, `_int`, `_digital`).

Utilize-a quando precisar popular leituras a partir de pares chave/valor extraídos do texto recebido.

---

## Classe `Events`
Também deriva de `Id` e adiciona três campos:

- `type`: categoria do evento (`EVENT_LEVEL`, `EVENT_COMMUNICATION` ou `EVENT_UNKNOWN`).
- `flag`: símbolos presentes no texto original (✅, ⚠️ etc.).
- `text`: descrição completa do alerta.

O método `__str__` inclui os metadados herdados para manter rastreabilidade nos logs.

---

## Classe `Decode`
Responsável por transformar `types.Message` em objetos de domínio:

1. Divide o texto da mensagem por linhas.
2. Tenta extrair `device_name` e os pares de valores utilizando `SetValues`.
3. Caso não seja leitura de valores, busca um evento (linha inicial com símbolos + linha de descrição) e infere o `event_type` pela presença de palavras-chave como "nível" ou "comunicação".
4. Expõe o resultado em `self.var_data`, que pode ser `Values`, `Events` ou `None`.

---

## Constantes disponibilizadas
- `EVENT_LEVEL`, `EVENT_COMMUNICATION`, `EVENT_UNKNOWN`
- `SYMBOL_CHECK`, `SYMBOL_WARNING`, `SYMBOL_DOWN_ARROW`, `SYMBOL_UP_ARROW`

Essas constantes são úteis para normalizar a interpretação dos alertas e os ícones recebidos das mensagens.

---

## Exemplo de uso
```python
from telebot import types
from sensorlog import Decode

def handle(message: types.Message):
    decoded = Decode(message)
    if decoded.var_data is None:
        return
    print(decoded.var_data)
```
