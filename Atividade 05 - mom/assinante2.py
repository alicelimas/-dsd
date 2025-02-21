import pika
import json


# Configuração da conexão com o RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost',  
    port=5672,
    credentials=pika.PlainCredentials('guest', 'guest')
))
channel = connection.channel()


# Declara o exchange do tipo topic
channel.exchange_declare(exchange='chat', exchange_type='topic', durable=True)


# Cria uma fila temporária exclusiva para este assinante
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue


# Assina todas as salas com o padrão "chat.*"
channel.queue_bind(exchange='chat', queue=queue_name, routing_key='chat.*')


# Função para processar mensagens recebidas
def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    room = method.routing_key.split('.')[1]
    print(f"[{room}] {message['sender']}: {message['message']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


# Configura o assinante
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)


print("Aguardando mensagens de todas as salas. Pressione CTRL+C para sair.")
channel.start_consuming()