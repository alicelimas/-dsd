from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields, Namespace
from flask_cors import CORS
import requests
import json

# Criar a instância do Flask
app = Flask(__name__)
CORS(app)

# Criar o Api do Flask-RESTX
api = Api(app, title='Fitness API Gateway', description='API para registrar atividades e calcular calorias')

# Modelo de dados pra entrada (usado na documentação do Swagger)
ns = Namespace('Atividades', description='Operações relacionadas a atividades')
api.add_namespace(ns)

atividade_model = api.model('Atividade', {
    'tipo': fields.String(required=True, description='Tipo de atividade (ex.: corrida, musculacao)'),
    'duracao': fields.Integer(required=True, description='Duração em minutos'),
    'intensidade': fields.String(required=True, description='Intensidade (leve, moderada, alta)')
})

# Função pra adicionar HATEOAS nas respostas
def add_hateoas(data, endpoint):
    links = {
        "self": f"/{endpoint}/{data.get('id', '')}",
        "atividades": "/atividades",
        "calcular_calorias": "/calcular_calorias"
    }
    return {**data, "links": links}

# Função pra carregar atividades do JSON
def carregar_atividades():
    try:
        with open('atividades.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Rota pra listar atividades (Flask puro)
@app.route('/atividades', methods=['GET'])
def listar_atividades():
    atividades = carregar_atividades()
    if not atividades:
        return jsonify({"mensagem": "Nenhuma atividade registrada", "links": {"self": "/atividades"}}), 200
    
    atividades_com_hateoas = [add_hateoas(atividade, "atividades") for atividade in atividades]
    return jsonify({"atividades": atividades_com_hateoas, "links": {"self": "/atividades"}}), 200

# Rota pra registrar uma atividade (Flask puro)
@app.route('/atividades', methods=['POST'])
def registrar_atividade():
    dados = request.get_json()
    id_atividade = len(carregar_atividades()) + 1
    atividade = {
        "id": id_atividade,
        "tipo": dados["tipo"],
        "duracao": dados["duracao"],
        "intensidade": dados["intensidade"]
    }
    
    response = requests.post("http://10.3.5.12:5001/atividades", json=atividade)
    if response.status_code != 201:
        return jsonify({"erro": "Falha ao salvar atividade"}), 500
    
    atividade_com_hateoas = add_hateoas(atividade, "atividades")
    return jsonify(atividade_com_hateoas), 201

# Rota pra calcular calorias (Flask puro)
@app.route('/calcular_calorias', methods=['POST'])
def calcular_calorias():
    dados = request.get_json()
    from zeep import Client
    client = Client('http://10.3.5.12:5002/?wsdl')
    calorias = client.service.calcular_calorias(
        tipo=dados["tipo"],
        duracao=dados["duracao"],
        intensidade=dados["intensidade"]
    )
    
    resultado = {"calorias": calorias}
    resultado_com_hateoas = add_hateoas(resultado, "calcular_calorias")
    return jsonify(resultado_com_hateoas), 200

# Adicionando rotas ao Swagger manualmente
@api.route('/atividades')
class AtividadesResource(Resource):
    @api.doc('listar_atividades')
    @api.response(200, 'Lista de atividades retornada com sucesso')
    def get(self):
        return listar_atividades()

    @api.doc('registrar_atividade')
    @api.expect(atividade_model)
    @api.response(201, 'Atividade registrada com sucesso')
    @api.response(500, 'Erro ao salvar atividade')
    def post(self):
        return registrar_atividade()

@api.route('/calcular_calorias')
class CalcularCaloriasResource(Resource):
    @api.doc('calcular_calorias')
    @api.expect(atividade_model)
    @api.response(200, 'Calorias calculadas com sucesso')
    def post(self):
        return calcular_calorias()

if __name__ == "__main__":
    app.run(host='10.3.5.12', port=5000)