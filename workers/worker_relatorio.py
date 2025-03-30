import pika
import json
import time
from datetime import datetime

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"📊 Gerando relatório diário de frequência...")

    # Simula tempo de geração
    time.sleep(3)

    # Aqui você geraria um relatório real com acesso ao banco de dados
    nome_arquivo = f"relatorio_frequencia_{datetime.now().strftime('%Y%m%d')}.csv"
    print(f"✔️ Relatório gerado: {nome_arquivo}")

    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="fila_relatorio", durable=True)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="fila_relatorio", on_message_callback=callback)

print("🎧 Aguardando mensagens para gerar relatórios...")
channel.start_consuming()
