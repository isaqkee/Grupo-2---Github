import os, json
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import pika

app = FastAPI(title="Smart 4.0 - Cobot Service (Grupo 2)", version="1.0.0")

RABBITMQ_HOST = "127.0.0.1"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "smart40_admin"
RABBITMQ_PASS = "Smart40Pass@2026"

class TaskRequest(BaseModel):
    task: str
    piece_id: str

@app.get("/api/v1/cobot/status")
def get_status():
    return {
        "connected": True,
        "robot_ip": "192.168.150.33",
        "gripper_ip": "192.168.150.34",
        "state": "OPERANDO",
        "tcp_cartesian": {"x": -216.12, "y": 171.02, "z": -91.34},
        "joints_rad": [0.0, -1.57, 0.0, -1.57, 0.0, 0.0],
        "gripper_closed": False,
        "max_stroke_mm": 40.87
    }

@app.post("/api/v1/cobot/tasks", status_code=status.HTTP_202_ACCEPTED)
def queue_task(task_req: TaskRequest):
    try:
        creds = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        conn = pika.BlockingConnection(pika.ConnectionParameters(
            host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=creds
        ))
        channel = conn.channel()
        channel.queue_declare(queue="cobot.tasks", durable=True)
        channel.basic_publish(
            exchange="",
            routing_key="cobot.tasks",
            body=json.dumps(task_req.model_dump()),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        conn.close()
        return {"status": "ENQUEUED", "data": task_req.model_dump()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
