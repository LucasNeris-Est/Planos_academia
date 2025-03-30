```markdown
# 🏋️‍♂️ Sistema de Gestão de Academia com FastAPI, RabbitMQ e Machine Learning

Este projeto é uma API REST para gerenciamento de alunos, check-ins, relatórios e previsão de churn em academias.  
Utiliza **FastAPI**, **RabbitMQ**, **PostgreSQL** e **Machine Learning** com **scikit-learn** para modelagem preditiva.

---

## 🚀 Funcionalidades

- Cadastro de alunos
- Registro de check-ins (manual e em massa via fila)
- Geração automática de relatórios diários
- Modelo de churn treinado com base nos dados reais
- Arquitetura assíncrona com workers e RabbitMQ
- API documentada automaticamente com Swagger (OpenAPI)

---

## 🧱 Estrutura do Projeto

```
PLANOS_ACADEMIA/
├── app/
│   ├── main.py              # Inicializa a API
│   ├── producer.py          # Envia mensagens para RabbitMQ
│   ├── routes/              # Endpoints REST
│   │   ├── alunos.py
│   │   ├── checkins.py
│   │   └── tarefas.py
├── workers/                 # Workers que escutam as filas
│   ├── worker_checkin.py
│   ├── worker_relatorio.py
│   └── worker_churn.py
├── modelos/                 # Modelos de churn salvos (.pkl)
├── relatorios/              # Relatórios diários gerados (.csv)
├── banco.json               # Configuração de conexão com PostgreSQL
├── requirements.txt
└── README.md
```

---

## 🛠️ Requisitos

- Python 3.10+
- PostgreSQL (rodando na porta 5433)
- RabbitMQ (com o painel ativo em `http://localhost:15672`)

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

4. Configure o banco de dados PostgreSQL:

- Crie o banco chamado `academia`
- Execute o script SQL para criar as tabelas (não incluído aqui)
- Preencha o arquivo `banco.json` com:

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

Acesse a documentação interativa:

📍 http://localhost:8000/docs

---

### 2. Inicie os workers (em terminais separados)

```bash
python workers/worker_checkin.py
python workers/worker_relatorio.py
python workers/worker_churn.py
```

---

### 3. Teste a aplicação com script

Você pode usar `test_api.py` (se criado) para registrar alunos, check-ins e acionar os workers via API:

```bash
python test_api.py
```

---

## 📂 Diretórios de saída

- 📄 Relatórios gerados: `relatorios/relatorio_frequencia_YYYYMMDD.csv`
- 🧠 Modelo treinado: `modelos/modelo_churn.pkl`

---

## 🔒 Segurança

- O arquivo `banco.json` **não deve ser versionado** (`.gitignore` configurado).
- Autenticação JWT pode ser adicionada com facilidade (em desenvolvimento).

---

## 📌 Futuras melhorias

- Integração com frontend em React ou Streamlit
- Exportação de relatórios em PDF
- Deploy com Docker + Docker Compose
- Agendamento automático de tarefas com Celery ou cron

---

## 🤝 Contribuição

Sinta-se à vontade para abrir issues, pull requests ou sugerir melhorias.

---

## 📜 Licença

MIT - Use livremente, com os devidos créditos.

---

```

---