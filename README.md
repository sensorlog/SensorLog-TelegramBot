# 🌐 SensorLog-TelegramBot

O **SensorLog-TelegramBot** expõe exemplos práticos para receber eventos dos sensores [sensor.log](https://sensor.log.br) através da API do Telegram e encaminhá-los para outros serviços. O objetivo principal é oferecer uma base consistente para integrações públicas: manter o formato dos objetos, garantir rastreabilidade com logs e permitir que cada exemplo seja facilmente adaptado para produção.

---

## 🚀 Recursos Principais
- Processamento imediato de mensagens recebidas em canais do Telegram utilizando `pyTelegramBotAPI`.
- Conversão dos textos enviados pelos sensores em objetos `Values` e `Events` com validação de tipos.
- Exemplos prontos para envio HTTP, persistência em SQLite e notificação em WhatsApp (CallMeBot).
- Logging padronizado em todos os scripts para facilitar depuração e auditoria.

---

## 🛠 Pré-requisitos
- **Python 3.9+**
- **pip** e **virtualenv** (opcional, porém recomendado)
- **Conta no Telegram** e um bot configurado via [BotFather](https://t.me/BotFather)
- Dependências listadas em [`requirements.txt`](requirements.txt)

---

## ⚙️ Instalação Rápida
```bash
git clone https://github.com/sensorlog/SensorLog-TelegramBot.git
cd SensorLog-TelegramBot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configuração compartilhada (`config.py`)
Todos os exemplos carregam os valores definidos em `config.py`. Você pode editar o arquivo diretamente ou exportar as variáveis de ambiente listadas abaixo antes de executar qualquer script.

| Campo | Variável de ambiente | Descrição |
| --- | --- | --- |
| Token do bot do Telegram | `TELEGRAM_TOKEN` | Credencial criada no BotFather. |
| URL para eventos HTTP | `EVENT_URL` | Endpoint que recebe objetos `Events` no exemplo `http_post.py`. |
| URL para valores HTTP | `VALUES_URL` | Endpoint que recebe objetos `Values` no exemplo `http_post.py`. |
| Nome do banco SQLite | `DB_NAME` | Caminho usado por `SQL_insert.py` e `create_db.py`. |
| API Key do CallMeBot | `CALLMEBOT_API_KEY` | Chave obtida no CallMeBot para o script `whatsapp.py`. |
| Telefone do CallMeBot | `CALLMEBOT_PHONE` | Número autorizado a receber as notificações via WhatsApp. |

Se nenhuma variável for exportada, o projeto utiliza os valores padrão presentes em `config.Settings`.

---

## 📂 Estrutura do Projeto
| Caminho | Descrição |
| --- | --- |
| `config.py` | Define as credenciais e URLs compartilhadas pelos exemplos (suporta variáveis de ambiente). |
| `sensorlog/` | Núcleo da biblioteca (classes `Id`, `Values`, `Events`, `SetValues` e `Decode`). |
| `basic.py` | Exemplo mínimo: imprime no console os dados recebidos. |
| `http_post.py` | Encaminha valores/eventos para endpoints HTTP. |
| `http_server.py` | FastAPI simples para receber as requisições enviadas por `http_post.py`. |
| `SQL_insert.py` | Persiste as leituras em SQLite. |
| `create_db.py` | Cria as tabelas `events` e `sensor_values`. |
| `whatsapp.py` | Encaminha eventos para o WhatsApp via CallMeBot. |
| `sensorlog/README.md` | Detalhes completos das classes expostas pelo pacote. |

---

## 🧱 Estrutura dos Objetos
### Values
Medições periódicas contendo dados de nível, temperatura, tensão, qualidade de sinal e entradas digitais. Cada leitura preserva metadados (canal, bot, dispositivo e timestamp).

### Events
Alertas gerados pelos sensores. Possuem `event_type`, `event_flag`, texto descritivo e a mesma base de metadados presentes em `Values`.

Detalhes completos das propriedades e conversões estão em [`sensorlog/README.md`](sensorlog/README.md).

---

## 📚 Exemplos Práticos
### ▶️ Exemplo Básico
1. Configure `TELEGRAM_TOKEN` em `config.py` (ou exporte a variável antes de iniciar).
2. Execute:
   ```bash
   python3 basic.py
   ```
3. Consulte o console: cada mensagem válida gera logs `INFO` delineando o fluxo e imprime o objeto `Values` ou `Events` correspondente.

### 🌐 HTTP POST + FastAPI
1. Ajuste `TELEGRAM_TOKEN`, `EVENT_URL` e `VALUES_URL` em `config.py` ou via variáveis de ambiente.
2. Inicie o servidor de testes (em outro terminal):
   ```bash
   uvicorn http_server:app --host 0.0.0.0 --port 9001
   ```
3. Rode:
   ```bash
   python3 http_post.py
   ```

### 💾 SQLite
1. Ajuste `TELEGRAM_TOKEN` e `DB_NAME` em `config.py` (ou exporte as variáveis).
2. Execute apenas na primeira vez para criar as tabelas:
   ```bash
   python3 create_db.py
   ```
3. Preencha a base com novos registros:
   ```bash
   python3 SQL_insert.py
   ```

### 📲 WhatsApp (CallMeBot)
1. Obtenha sua `API_KEY` seguindo [as instruções do CallMeBot](https://www.callmebot.com/blog/free-api-whatsapp-messages/).
2. Ajuste `TELEGRAM_TOKEN`, `CALLMEBOT_API_KEY` e `CALLMEBOT_PHONE` em `config.py` ou exporte-os.
3. Execute e verifique os envios:
   ```bash
   python3 whatsapp.py
   ```

> **Importante:** O CallMeBot só entrega mensagens para o número que gerou a `API_KEY`. Esta integração é indicada para notificações pessoais.

---

## 📝 Boas Práticas
- Não exponha tokens ou chaves privadas no repositório; utilize variáveis de ambiente quando possível.
- Todos os exemplos utilizam `logging`. Ajuste o `logging.basicConfig` conforme sua necessidade (arquivo, nível, formato).
- Revise e adapte as funções `process_channel_message_*` para aplicar regras de negócio específicas.

---

## 📜 Documentação Complementar
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [PyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- [sensorlog/README.md](sensorlog/README.md) — Referência das classes que estruturam os dados.

---

## 🤝 Contribuição
Contribuições são bem-vindas! Abra uma issue ou envie um pull request descrevendo problemas, melhorias ou novos exemplos.

## 📄 Licença
Este projeto está licenciado sob a [MIT License](LICENSE).
