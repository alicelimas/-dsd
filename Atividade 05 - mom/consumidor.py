import pika

# Estabelece conexão com o RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='localhost',
    port=5672,
    credentials=pika.PlainCredentials('guest', 'guest')
))
channel = connection.channel()

# Declara a fila (para garantir que existe)
channel.queue_declare(queue='minha_fila', durable=True)

# Função para processar mensagens recebidas
def callback(ch, method, properties, body):
    print(f"Mensagem recebida: {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Configura o consumidor
channel.basic_consume(
    queue='minha_fila',
    on_message_callback=callback,
    auto_ack=False
)

print("Aguardando mensagens. Pressione CTRL+C para sair.")
channel.start_consuming()