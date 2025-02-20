from flask import Flask, request, jsonify
import pika

app = Flask(__name__)

# Configuração da conexão com o RabbitMQ
def get_rabbitmq_connection():
    credentials = pika.PlainCredentials('guest', 'guest')  
    parameters = pika.ConnectionParameters(
        host='localhost',  
        port=5672,
        credentials=credentials
    )
    return pika.BlockingConnection(parameters)

# Rota para publicar mensagens na fila
@app.route('/rabbitmq', methods=['POST'])
def publish_message():
    try:
        # Obtém os dados da requisição
        data = request.get_json()
        message = data.get('message')

        if not message:
            return jsonify({'error': 'message é obrigatório'}), 400

        # Conecta ao RabbitMQ
        connection = get_rabbitmq_connection()
        channel = connection.channel()

        # Declara a fila (cria se não existir)
        channel.queue_declare(queue='minha_fila', durable=True)

        # Publica a mensagem na fila
        channel.basic_publish(
            exchange='',  
            routing_key='minha_fila',  # Nome da fila
            body=message.encode(),
            properties=pika.BasicProperties(delivery_mode=2)  # Persistência
        )
        connection.close()

        return jsonify({'message': 'Mensagem publicada na fila com sucesso'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Inicia a API
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)