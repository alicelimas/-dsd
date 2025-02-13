from spyne import Application, rpc, ServiceBase, Integer, Unicode, Float
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

class CalculadoraCalorias(ServiceBase):
    @rpc(Unicode, Integer, Unicode, _returns=Float)
    def calcular_calorias(ctx, tipo, duracao, intensidade):
        # Valores MET aproximados
        mets = {
            "corrida": {"leve": 6.0, "moderada": 7.0, "alta": 8.3},
            "caminhada": {"leve": 2.0, "moderada": 3.5, "alta": 4.5},
            "ciclismo": {"leve": 4.0, "moderada": 6.0, "alta": 8.0},
            "natacao": {"leve": 5.0, "moderada": 6.0, "alta": 8.0},
            "futebol": {"leve": 5.0, "moderada": 7.0, "alta": 10.0},
            "musculacao": {"leve": 3.0, "moderada": 4.5, "alta": 6.0}
        }
        met = mets.get(tipo.lower(), {}).get(intensidade.lower(), 3.5)
        peso = 70  # Peso padrão (em kg)
        calorias = met * peso * (duracao / 60)
        return calorias

application = Application(
    [CalculadoraCalorias],
    tns='fitness.soap',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

if __name__ == '__main__':
    wsgi_app = WsgiApplication(application)
    server = make_server('10.3.5.12', 5002, wsgi_app)
    print("Servidor SOAP rodando na porta 5002.")
    server.serve_forever()
    
    