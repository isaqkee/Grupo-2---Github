import json, pika

RABBITMQ_HOST = "127.0.0.1"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "smart40_admin"
RABBITMQ_PASS = "Smart40Pass@2026"
QUEUE_NAME = "cobot.inspections"

def callback(ch, method, properties, body):
    data = json.loads(body.decode("utf-8"))
    piece = data.get("piece_id")
    verdict = data.get("verdict")
    target = data.get("target_destination")
    print(f"\n[Robô UR Acionado]")
    print(f" -> Peça: {piece}")
    print(f" -> Qualidade: {data.get('quality_score')}% ({verdict})")
    print(f" -> Movimento: Enviando peça para {target}!")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    creds = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    conn = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=creds
    ))
    channel = conn.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    print("[Robô UR Ativo] Aguardando mensagens de inspeção do RabbitMQ... (Pressione Ctrl+C para sair)")
    channel.start_consuming()

if __name__ == "__main__":
    main()
