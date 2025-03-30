# 🏋️‍♂️ Sistema de Gestão de Academia com FastAPI, RabbitMQ e Machine Learning

Este projeto é uma API REST para gerenciamento de alunos, check-ins, saídas (checkouts), geração de relatórios e previsão de churn em academias.  
Utiliza **FastAPI**, **RabbitMQ**, **PostgreSQL** e **scikit-learn** para modelagem preditiva com **Random Forest**.

---

## 🚀 Funcionalidades

- Cadastro de alunos
- Registro de check-ins manuais e em massa (via fila)
- Registro de saída (checkout) manual e em massa (via fila)
- Geração automática de relatórios diários
- Modelo preditivo de churn com base em:
  - Tempo desde o último check-in
  - Frequência semanal
  - Duração média das visitas
  - Tipo de plano
- Arquitetura assíncrona com filas e workers via RabbitMQ
- API documentada automaticamente com Swagger (OpenAPI)

---

## 🧱 Estrutura do Projeto

```
PLANOS_ACADEMIA/
├── app/
│   ├── main.py                # Inicialização da API
│   ├── producer.py            # Envio de mensagens para RabbitMQ
│   └── routes/
│       ├── alunos.py          # Endpoints de alunos
│       ├── checkins.py        # Endpoints de entrada
│       ├── checkouts.py       # Endpoints de saída
│       └── tarefas.py         # Endpoints para acionar as filas
├── modelos/
│   └── modelo_churn.pkl       # Modelo treinado
├── relatorios/
│   └── relatorio_frequencia_YYYYMMDD.csv
├── scripts/
│   ├── Criacao_banco_academia.py
│   ├── Alimentacao_banco.py
│   └── test_api.py            # Script para testes completos
├── workers/
│   ├── worker_checkin.py
│   ├── worker_checkout.py
│   ├── worker_relatorio.py
│   └── worker_churn.py
├── banco.json                 # Configurações do banco (ignorado no git)
├── requirements.txt
└── README.md
```

---

## 🛠️ Requisitos

- Python 3.10+
- PostgreSQL (rodando na porta 5433)
- RabbitMQ (painel acessível em `http://localhost:15672`)

---

## 📦 Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seuusuario/seuprojeto.git
cd PLANOS_ACADEMIA
```

2. Crie e ative o ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate     # Windows
# ou
source .venv/bin/activate  # Linux/macOS
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure o banco de dados:

```bash
python scripts/Criacao_banco_academia.py
python scripts/Alimentacao_banco.py  # opcional
```

5. Crie e preencha o arquivo `banco.json`:

```json
{
  "host": "localhost",
  "dbname": "academia",
  "user": "postgres",
  "password": "sua_senha",
  "port": 5433
}
```

---

## 🧪 Executando o projeto

### 1. Inicie a API

```bash
fastapi dev app.main
```

Acesse a documentação:

📍 http://localhost:8000/docs

---

### 2. Inicie os workers (em terminais separados)

```bash
python workers/worker_checkin.py
python workers/worker_checkout.py
python workers/worker_relatorio.py
python workers/worker_churn.py
```

---

### 3. Teste a aplicação com o script de integração

```bash
python scripts/test_api.py
```

---

## 📂 Diretórios de saída

- 📁 `relatorios/`: CSVs de frequência diários
- 📁 `modelos/`: modelo preditivo de churn treinado

---

## 🔒 Segurança

- O arquivo `banco.json` **está no `.gitignore`** e não deve ser versionado.
- Sistema preparado para incluir autenticação JWT.

---

## 📌 Futuras melhorias

- Interface com Streamlit ou React
- Exportação de relatórios em PDF
- Deploy com Docker + Docker Compose
- Tarefas agendadas com Celery ou cron jobs
- Monitoramento com Prometheus + Grafana

---
