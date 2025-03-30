import pika
import json
import time

def callback(ch, method, properties, body):
    data = json.loads(body)
    print("🧠 Atualizando modelo de churn...")

    # Simula tempo de treino/atualização do modelo
    time.sleep(5)

    # Aqui você carregaria dados, reentreinaria ou ajustaria o modelo real
    print("✔️ Modelo de churn atualizado com sucesso.")

    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="fila_churn", durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="fila_churn", on_message_callback=callback)

print("🎧 Aguardando mensagens para atualizar modelo de churn...")
channel.start_consuming()
