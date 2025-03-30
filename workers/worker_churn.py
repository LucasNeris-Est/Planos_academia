import pika
import json
import psycopg2
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

# ---------------------------
# Configuração do banco
# ---------------------------
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "banco.json")
with open(config_path, "r") as f:
    db_config = json.load(f)

def get_connection():
    return psycopg2.connect(**db_config)

# ---------------------------
# Função principal de atualização do modelo
# ---------------------------
def atualizar_modelo():
    print("🧠 Coletando dados de frequência...")
    con = get_connection()

    query = """
        SELECT aluno_id, MAX(data_checkin) as ultimo_checkin
        FROM checkins
        GROUP BY aluno_id
    """
    df = pd.read_sql_query(query, con)
    con.close()

    df["dias_sem_checkin"] = (datetime.now() - df["ultimo_checkin"]).dt.days
    df["churn"] = df["dias_sem_checkin"].apply(lambda d: 1 if d > 15 else 0)

    X = df[["dias_sem_checkin"]]
    y = df["churn"]

    print("🤖 Treinando modelo de churn...")
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X, y)

    # Salvar o modelo
    if not os.path.exists("modelos"):
        os.makedirs("modelos")

    with open("modelos/modelo_churn.pkl", "wb") as f:
        pickle.dump(modelo, f)

    print("✅ Modelo de churn atualizado e salvo com sucesso.")

# ---------------------------
# Callback da fila
# ---------------------------
def callback(ch, method, properties, body):
    print("🧠 Atualizando modelo de churn com base nos dados reais...")
    atualizar_modelo()
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="fila_churn", durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="fila_churn", on_message_callback=callback)

print("🎧 Aguardando mensagens para atualizar modelo de churn...")
channel.start_consuming()
