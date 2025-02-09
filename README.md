# 🌐 SensorLog-TelegramBot

Bem-vindo ao **SensorLog-TelegramBot**! Este projeto foi desenvolvido para integrar, de forma rápida e fácil, os sensores da [sensor.log](https://sensor.log.br) com outros sistemas.  
A integração com o sistema de [sensor.log](https://sensor.log.br) é feita através do uso da **API do Telegram**, e nesse repositório são disponibilizados exemplos práticos para envio desses dados para outras aplicações.

---

## 📋 Índice

- [📖 Introdução](#-introdução)
- [🛠 Pré-requisitos](#-pré-requisitos)
- [⚙️ Instalação](#️-instalação)
- [🔧 Configuração](#-configuração)
  - [🔑 Obtenção do Token do Bot no Telegram](#-obtenção-do-token-do-bot-no-telegram)
  - [📩 Adicionando o Bot ao Canal de Log](#-adicionando-o-bot-ao-canal-de-log)
- [📂 Estrutura do Projeto](#-estrutura-do-projeto)
- [✍️ Estrutura dos Objetos](#-estrutura-dos-objetos)
  - [📊 Estrutura de "Values"](#-estrutura-de-values)
  - [⚡ Estrutura de "Events"](#-estrutura-de-events)
- [📚 Exemplos de Uso](#-exemplos-de-uso)
  - [▶️ Exemplo Básico](#️-exemplo-básico)
  - [🌐 Exemplo HTTP POST](#-exemplo-http-post)
  - [💾 Exemplo de Inserção em Banco de Dados SQLite](#-exemplo-de-inserção-em-banco-de-dados-sqlite)
  - [📲 Exemplo de integração com WhatsApp via CallMeBot](#-exemplo-de-integração-com-whatsapp-via-callmebot)
- [📜 Documentação Oficial da API do Telegram](#-documentação-oficial-da-api-do-telegram)
- [🤝 Contribuição](#-contribuição)
- [📜 Licença](#-licença)

---

## 📖 Introdução

O **SensorLog-TelegramBot** permite que você:

- 🛰 Receba e processe eventos de sensores enviados para um canal do Telegram.
- 🔗 Integre esses dados com sistemas externos, APIs ou bancos de dados.
- ⚙️ Implemente funcionalidades personalizadas para monitoramento e automação.

---

## 🛠 Pré-requisitos

Antes de começar, certifique-se de ter:

- **Python 3.7 ou superior**: [Baixe aqui](https://www.python.org/downloads/).
- **Git**: Para clonar o repositório. [Baixe aqui](https://git-scm.com/).
- **Virtualenv** (opcional): Para criar um ambiente isolado de desenvolvimento.
- **Conta no Telegram**: Para configurar e gerenciar o bot.

---

## ⚙️ Instalação

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/sensorlog/SensorLog-TelegramBot.git
   ```
   ```bash
   cd SensorLog-TelegramBot
   ```

2. **Crie um ambiente virtual:**

   ```bash
   python3 -m venv .venv
   ```
   ```bash
   source .venv/bin/activate
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

---

## 🔧 Configuração

### 🔑 Obtenção do Token do Bot no Telegram

1. **Inicie uma conversa com o BotFather:**
   - No aplicativo do Telegram, procure por `@BotFather` e selecione o bot oficial (verificado com um ícone azul).
   - Toque em "Iniciar" para começar a conversa.

2. **Crie um novo bot:**
   - Envie o comando `/newbot` no chat com o BotFather.
   - Siga as instruções fornecidas para:
     - **Definir um nome para o seu bot**: Por exemplo, `integrador_sensorlog`.
     - **Definir um nome de usuário para o bot**: Deve terminar com `bot`, por exemplo, `integrador_sensorlog_bot`.

3. **Obtenha o token do bot:**
   - Após configurar o nome e o nome de usuário, o BotFather fornecerá um token de API no formato:
     ```
     123456789:ABCdEfGhIjKlMnOpQrStUvWxYz123456789
     ```
   - Guarde este token em um local seguro, pois ele é essencial para conectar o seu bot à API do Telegram.

4. **Nota de Segurança:**
   - 🔒 Não compartilhe seu token publicamente.
   - ⚠️ Caso suspeite que ele foi comprometido, use o comando `/revoke` no BotFather para gerar um novo token.

### 📩 Adicionando o Bot ao Canal de Log

Adicione seu bot a um canal de LOG de onde deseja receber os dados dos sensores.

---

## 📂 Estrutura do Projeto

- **`basic.py`**: Processa eventos do Telegram e exibe os dados no console.
- **`http_post.py`**: Envia dados para URLs específicas usando HTTP POST.
- **`http_server.py`**: Recebe os dados enviados por http_post.py.
- **`SQL_insert.py`**: Insere dados recebidos em um banco de dados SQLite.
- **`create_db.py`**: Script para criar o banco de dados e as tabelas necessárias.
- **`whatsapp.py`**: Envia os eventos recebidos para o WhatsApp.
- **`sensorlog/`**: Módulos para processamento de eventos e valores dos sensores.

---

## ✍️ Estrutura dos Objetos

### 📊 Estrutura de "Values"

O objeto **`Values`** representa os valores lidos pelo dispositivo e contém os seguintes campos:

- **Identificação e origem:**
  - `channel_id`: ID único do canal no Telegram.
  - `channel_name`: Nome do canal, utilizado para identificar o cliente.
  - `bot_name`: Nome do bot, que funciona como gateway de comunicação.
  - `device_name`: Nome do reservatório.

- **Medições do reservatório:**
  - `level`: Nível do reservatório processado (float ou `None`).
  - `raw_level`: Nível bruto do reservatório antes do processamento (float ou `None`).
  - `distance`: Distância entre o transdutor e a superfície da água (float ou `None`).

- **Taxas de variação:**
  - `speed1`: Primeira taxa de variação do nível do reservatório (int ou `None`).
  - `speed2`: Segunda taxa de variação do nível do reservatório (int ou `None`).

- **Leituras adicionais do terminal:**
  - `t0`: Temperatura inicial medida pelo terminal (float ou `None`).
  - `t1`: Temperatura final medida pelo terminal (float ou `None`).
  - `v0`: Tensão inicial da bateria do terminal (float ou `None`).
  - `v1`: Tensão final da bateria do terminal (float ou `None`).

- **Qualidade do sinal:**
  - `snr`: Relação sinal-ruído recebida pelo terminal (int ou `None`).
  - `rssi`: Intensidade do sinal recebido pelo terminal (int ou `None`).
  - `snr_gw`: Relação sinal-ruído recebida pelo gateway (int ou `None`).
  - `rssi_gw`: Intensidade do sinal recebido pelo gateway (int ou `None`).

- **Indicação de horário:**
  - `time`: Momento em que a leitura foi registrada no telegram.
  - `timezone_offset`: Diferença de fuso horário aplicada a leitura.


### ⚡ Estrutura de "Events"

O objeto **`Events`** representa eventos do sistema e contém os seguintes campos:

- **Identificação e origem:**
  - `channel_id`: ID único do canal no Telegram.
  - `channel_name`: Nome do canal, utilizado para identificar o cliente.
  - `bot_name`: Nome do bot que funciona como gateway de comunicação.
  - `device_name`: Nome do dispositivo associado ao evento.

- **Informações do evento:**
  - `event_type`: Tipo do evento (inteiro representando a categoria do evento).
  - `event_flag`: Indicador opcional associado ao evento (string).
  - `event_text`: Descrição do evento (string).

- **Indicação de horário:**
  - `time`: Momento em que o evento foi registrado no telegram.
  - `timezone_offset`: Diferença de fuso horário aplicada ao evento.


### 🛈 Mais detalhes sobre os objetos acesse a [documentação específica](./sensorlog/README.md)

---

## 📚 Exemplos de Uso

### ▶️ Exemplo Básico

1. Configure o token no arquivo `basic.py`:
   ```python
   TOKEN = "SEU_TOKEN_AQUI"
   ```

2. Execute o script:
   ```bash
   python basic.py
   ```

3. Verifique os logs no console.

### 🌐 Exemplo HTTP POST

1. Configure o token e as URLs no arquivo `http_post.py`:
   ```python
   TOKEN = "SEU_TOKEN_AQUI"
   EVENT_URL = "http://localhost:9001/events"
   VALUES_URL = "http://localhost:9001/values"
   ```

2. Execute em um terminal o script para rodar o servidor http que recebe os eventos e valores dos sensores:
   ```bash
   python http_server.py
   ```

3. Execute em outro terminal o script para enviar ao servidor os eventos e valores recebidos do Telegram:
   ```bash
   python http_post.py
   ```

4. Os dados serão enviados para as URLs configuradas.

### 💾 Exemplo de Inserção em Banco de Dados SQLite

1. Configure o token e o banco no arquivo `SQL_insert.py`:
   ```python
   TOKEN = "SEU_TOKEN_AQUI"
   DB_NAME = "sensordata.db"
   ```

2. Configure o banco de dados (**apenas na primeira vez** que for usar SQL_insert.py).
   Execute o script `create_db.py` para criar a base de dados e as tabelas necessárias:
   ```bash
   python create_db.py
   ```

3. Execute o script:
   ```bash
   python SQL_insert.py
   ```

4. Os dados serão salvos no banco SQLite.


### 📲 Exemplo de integração com WhatsApp via CallMeBot

#### "Somente para uso pessoal"
É possível enviar notificações para o **WhatsApp** utilizando a API do **CallMeBot**. Essa funcionalidade permite que eventos recebidos do Telegram sejam encaminhados **apenas para o seu número** de telefone via WhatsApp.

#### 🔑 Como obter a API_KEY do CallMeBot

Siga os passos abaixo para obter sua **API_KEY**:

1. Adicione o número do CallMeBot aos seus contatos do WhatsApp:
   ```
   +34 684 783 708
   ```

2. No WhatsApp, envie a seguinte mensagem para o número salvo:
   ```
   I allow callmebot to send me messages
   ```

3. Aguarde a resposta:
   - O CallMeBot responderá com sua API_KEY exclusiva, que será necessária para enviar mensagens.
   - Aguarde até 2 minutos para receber a resposta, se não receber, tente novamente depois de 24h.

4. Configure o TELEGRAM_TOKEN, API_KEY e PHONE no arquivo `whatsapp.py`:
   ```python

   TELEGRAM_TOKEN = "SEU_TOKEN_AQUI"
   API_KEY = "SEU_API_KEY_CALLMEBOT"
   PHONE = "SEU_NUMERO_TELEFONE"
   ```

5. Execute o script
   ```bash
   python whataspp.py
   ```

6. Os eventos serão enviados para seu telefone via WhatsApp.

---

## 📜 Documentação Oficial da API do Telegram

Para mais informações sobre as funcionalidades da API do Telegram, consulte a documentação oficial:  
[Telegram Bot API Documentation](https://core.telegram.org/bots/api)

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorar este projeto.

---

## 📜 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
