import pika
import json
import time

def callback(ch, method, properties, body):
    data = json.loads(body)
    print("✅ Processando check-ins em massa...")
    time.sleep(2)
    # Aqui você acessaria o banco e executaria sua lógica
    print("✔️ Check-ins processados.")
    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="fila_checkin", durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="fila_checkin", on_message_callback=callback)

print("🎧 Aguardando mensagens para processar check-ins...")
channel.start_consuming()