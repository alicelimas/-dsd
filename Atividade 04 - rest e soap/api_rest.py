from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Função pra carregar e salvar atividades no JSON
def carregar_atividades():
    try:
        with open('atividades.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def salvar_atividades(atividades):
    with open('atividades.json', 'w') as f:
        json.dump(atividades, f, indent=4)

# Rota pra registrar uma atividade
@app.route('/atividades', methods=['POST'])
def registrar_atividade():
    dados = request.get_json()
    atividades = carregar_atividades()
    atividades.append(dados)
    salvar_atividades(atividades)
    return jsonify({"mensagem": "Atividade registrada"}), 201

if __name__ == "__main__":
    app.run(host='10.3.5.12', port=5001)
    
    