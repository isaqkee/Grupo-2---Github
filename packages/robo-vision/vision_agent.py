import os, sys, time, json, uuid, cv2, pika
from pyzbar.pyzbar import decode

RABBITMQ_HOST = "127.0.0.1"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "smart40_admin"
RABBITMQ_PASS = "Smart40Pass@2026"
QUEUE_NAME = "cobot.inspections"

def get_channel():
    creds = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    conn = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=creds
    ))
    channel = conn.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    return channel, conn

def inspect_frame(frame, channel):
    decoded = decode(frame)
    if not decoded:
        return None
    for obj in decoded:
        qr_text = obj.data.decode("utf-8")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        variance = cv2.Laplacian(gray, cv2.CV_64F).var()
        score = round(min(max((variance / 250.0) * 100.0, 0.0), 100.0), 2)
        verdict = "INSPECTED_OK" if score >= 80.0 else "INSPECTED_NOK"
        target = "EXPEDICAO" if verdict == "INSPECTED_OK" else "REFUGO"

        payload = {
            "correlation_id": str(uuid.uuid4()),
            "piece_id": qr_text,
            "quality_score": score,
            "verdict": verdict,
            "target_destination": target,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        channel.basic_publish(
            exchange="", routing_key=QUEUE_NAME, body=json.dumps(payload),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        print(f"[Resultado] Peça: {qr_text} | Score: {score}% | Status: {verdict} -> Destino: {target}")
        return payload

if __name__ == "__main__":
    channel, conn = get_channel()
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        img = cv2.imread(sys.argv[1])
        inspect_frame(img, channel)
        conn.close()
        sys.exit(0)
    print("Passe o arquivo gerado: python vision_agent.py qr_sample_ok.png")
    conn.close()
