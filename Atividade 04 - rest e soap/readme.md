# Projeto de Sistema de Registro de Atividade Física com REST e SOAP

Este é um sistema que utiliza REST e SOAP para comunicação entre servidores Python e um cliente web em JavaScript, com um API Gateway centralizando as operações. O sistema permite que os usuários registrem atividades físicas, calculem calorias gastas e consultem a lista de atividades registradas, usando HATEOAS pra navegação dinâmica.

## Estrutura do Projeto

- `gateway.py`: Implementação do API Gateway em Python, usando Flask e Flask-RESTX, que gerencia requisições REST e chama serviços backend.
- `api_rest.py`: Implementação do servidor REST em Python, usando Flask, pra armazenar atividades em JSON.
- `api_soap.py`:  Implementação do servidor SOAP em Python, usando Spyne, pra calcular calorias com base em MET. 
- `index.html`: Cliente web em JavaScript, pra interação do usuário via navegador.
- `soap_client.js`:  Cliente SOAP em JavaScript (Node.js), pra testar o serviço SOAP diretamente.Mas somente para fins de teste.
- `atividades.json`: Arquivo JSON pra persistência das atividades registradas.

## Tecnologias Utilizadas

- **Python**: Usado pra implementar o Gateway, a API REST e a API SOAP, processando requisições e cálculos.
- **Node.js**: Ambiente de execução no navegador (via HTML) e no Node.js (pra cliente SOAP), pra interação do usuário e consumo de serviços.
- **Flask**: Framework web Python pra criar servidores REST e o Gateway.
- **Flask-RESTX**: Extensão do Flask pra documentação automática via Swagger.
- **Spyne**: Biblioteca Python pra criar serviços SOAP.
- **Zeep**: Biblioteca Python pra consumir serviços SOAP, usada no Gateway.
- **REST**: Estilo arquitetural pra comunicação leve e escalável, usado na API REST e Gateway.
- **SOAP**: Protocolo baseado em XML pra comunicação robusta, usado na API de cálculo de calorias.
- **HATEOAS**: Implementado no Gateway pra navegação dinâmica via links nas respostas.

## Pré-requisitos

Antes de começar, certifique-se de que você tem o seguinte instalado:

- **Python** (versão 3.6 ou superior)
- **Node.js** (versão 14 ou superior)

## Configuração do Servidor

Antes de tudo, certifique-se de estar no diretório de Atividade 04 - rest e soap.
```
cd . -dsd\Atividade 04 - rest e soap\
```

1. **Criação e ativação de ambiente virtual**
    ```
    python -m venv venv
    ```
    Para ativá-la, rodamos o seguinte comando:
    ```
    venv\Scripts\activate
    ```

2. **Instalação das dependências do Python**
    1. Você pode simplesmente instalar a partir do arquivo de requirements.txt, através do seguinte comando:
    ```
    pip install -r requirements.txt
    ```
    2. Ou, se preferir, pode instalar manualmente, executando o seguinte comando:
    ```
    pip install Flask Flask-RESTX flask-cors requests zeep spyne
    ```
    Para verificar se as bibiliotecas foram instaladas corretamente, execute:
    ```
    pip list 
    ```

2. **Altere o endereço ip do servidor nos seguintes códigos:**
   
    Caso não saiba o ip da máquina onde o servidor será executado, rode o seguinte comando no cmd:
    ```
    ipconfig
    ```
    Após isso, no **gateway.py**, substitua o trecho onde apresenta o endereço abaixo, pelo endereço ip encontrado.
    ```
    app.run(host='10.3.5.12', port=5000) 
    ```
     No arquivo **api_rest.py**, substitua o seguinte trecho pelo endereço ip correto:
    ```
    app.run(host='10.3.5.12', port=5001) 
    ```
     Em **api_soap.py**, altere:
    ```
    server = make_server('10.3.5.12', 5002, wsgi_app) 
    ```
3. **Inicie os servidores**

    Após tudo isso, você poderá executar os servidores. Rode cada servidor em terminais separados (caso esteja rodando na máquina vitual, lembre-se de ativá-la):
    - **Gateway:**
    ```
    python gateway.py
    ```
     - **API REST:**
    ```
    python api_rest.py
    ```
     - **API SOAP:**
    ```
    python api_soap.py
    ```


## Configuração do Cliente

1. **Altere o endereço ip do servidor no cliente:**
   
    Semelhantemente ao processo feito no servidor, você deve alterar o endereço pelo endereço real da máquina onde o servidor está sendo executado.
    No index.html, as URLs estão configuradas para http://10.3.5.12:5000, o que reflete o IP configurado. Se mudares o IP, atualize:
    ```    
    const response = await fetch('http://10.3.5.12:5000/atividades', 
    ```
    ```    
    const caloriasResponse = await fetch('http://10.3.5.12:5000/calcular_calorias',  
    ```
    ```    
    const response = await fetch('http://10.3.5.12:5000/atividades',
    ```

2. **Execute o cliente:**

    Abra o **index.html** no navegador da máquina cliente. Pode ser diretamente do sistema de arquivos (arrastando pro navegador).

    **Somente para caso de teste, se você desejar, realize o passo 3:**

3. **Configuração do Cliente SOAP**

    No **soap_client.js**, altere a URL do WSDL pra usar o IP do servidor:
    ```
    const url = 'http://10.3.5.12:5002/?wsdl';
    ```

4. **Instale as Dependências**

    Em outro terminal, destinado ao cliente SOAP, instale a seguinte dependência:
    ```
    npm install soap
    ```
5. **Execute o cliente soap:**

    Rode o script:
    ```
    node soap_client.js
    ```
Link para apresentação de slides: [Apresentação no Canva](https://www.canva.com/design/DAGe-88ijjg/OWNRjBdNVpSuSrDObiq1Vg/edit?utm_content=DAGe-88ijjg&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
