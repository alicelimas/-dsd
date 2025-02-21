from flask import Flask, request, jsonify
import pika
import json


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


# Rota para enviar mensagens ao chat
@app.route('/chat', methods=['POST'])
def send_message():
    try:
        # Obtém os dados da requisição
        data = request.get_json()
        room = data.get('room')  
        sender = data.get('sender')  
        message = data.get('message')  


        if not (room and sender and message):
            return jsonify({'error': 'room, sender e message são obrigatórios'}), 400


        # Monta a mensagem como JSON
        chat_message = {
            "sender": sender,
            "message": message
        }


        # Conecta ao RabbitMQ
        connection = get_rabbitmq_connection()
        channel = connection.channel()


        # Declara o exchange do tipo topic
        channel.exchange_declare(exchange='chat', exchange_type='topic', durable=True)


        # Publica a mensagem com a chave de roteamento (ex.: "chat.sala1")
        channel.basic_publish(
            exchange='chat',
            routing_key=f"chat.{room}",
            body=json.dumps(chat_message).encode(),
            properties=pika.BasicProperties(delivery_mode=2)  # Persistência
        )
        connection.close()


        return jsonify({'message': f'Mensagem enviada para a sala {room}'}), 200


    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Inicia a API
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
