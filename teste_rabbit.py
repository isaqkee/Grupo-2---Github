import pika

# Cole sua URL do CloudAMQP aqui embaixo
# amqp_url = 'amqps://iprmcicd:***@fuji.lmq.cloudamqp.com/iprmcicd'
amqp_url = 'amqps://tkignjsf:L3GohvHuWPA6w5PeVpSvjLQspXa9kfcx@jackal.rmq.cloudamqp.com/tkignjsf'
params = pika.URLParameters(amqp_url)
connection = pika.BlockingConnection(params)
channel = connection.channel()

print("Conectado ao RabbitMQ na Nuvem com sucesso!")

# Teste: Criar uma fila e enviar uma mensagem
channel.queue_declare(queue='teste')
channel.basic_publish(exchange='', routing_key='teste', body='Ola RabbitMQ!')
print("Mensagem enviada com sucesso!")

connection.close()
