# Projeto de sistema de votação com gRPC

Este é um sistema simples de votação que utiliza gRPC para comunicação entre um servidor Python e um cliente Node.js. O sistema permite que os usuários votem em candidatos e consultem os resultados.

## Estrutura do Projeto

- `cliente.js`: Implementação do cliente em Node.js.
- `server.py`: Implementação do servidor gRPC em Python.
- `voting.proto`: Arquivo de definição do protocolo (usando **Protocol Buffers**), que descreve as mensagens e os serviços gRPC. 

## Tecnologias Utilizadas

- **Python**: Para implementar o servidor que processa os votos.
- **Node.js**: Ambiente de execução JavaScript usado para implementar o cliente que interage com o servidor.
- **gRPC**: Comunicação remota de alto desempenho entre o servidor Python e o cliente Node.js.

## Pré-requisitos

Antes de começar, certifique-se de que você tem o seguinte instalado:

- **Python** (versão 3.6 ou superior)
- **Node.js** (versão 14 ou superior)

## Configuração do Servidor

Antes de tudo, certifique-se de estar no diretório de Atividade - gRPC.
```
cd . -dsd\Atividade - gRPC\
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
    2. Ou pode instalar executando o seguinte comando:
    ```
    pip install grpcio grpcio-tools
    ```
    Para verificar se as bibiliotecas foram instaladas corretamente, execute:
    ```
    pip list 
    ```

2. **Altere o endereço ip do servidor no código do servidor:**
   
    Caso não saiba o ip da máquina onde o servidor será executado, rode o seguinte comando no cmd:
    ```
    ipconfig
    ```
    Após isso, substitua o trecho onde apresenta o endereço abaixo, pelo endereço ip encontrado.
    ```
    server.add_insecure_port('10.3.5.12:50051') 
    ```
3. **Gere os arquivos proto**

    A partir do arquivo proto, você irá rodar o seguinte comando (ainda em ambiente virtual), para a geração de 2 arquivos:
    ```
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. voting.proto
    ```
    - **voting_pb2.py**: Contém as classes Python para as mensagens
    - **voting_pb2_grpc.py**: Contém as classes Python para os serviços gRPC

5. **Inicie o servidor:**
    Após tudo isso, você poderá executar o servidor:

    python server.py

## Configuração do Cliente

1. **Altere o endereço ip do servidor no cliente:**
   
    Semelhantemente ao processo feito no servidor, você deve alterar o endereço pelo endereço real da máquina onde o servidor está sendo executado.
    Sendo assim, substitua o endereço da seguinte linha, pelo endereço ip adequado:
    ```    
    const client = new votingProto("10.3.5.12:50051", grpc.credentials.createInsecure());
    ```

2. **Instale as Dependências**

    Em outro terminal, destinado ao cliente, rode o seguinte comando:
    ```
    npm install @grpc/grpc-js @grpc/proto-loader
    ```

3. **Execute o cliente:**
    ```
    node cliente.js
    ```
 
PDF com a apresentação de slides: [Apresentação - gRPC](https://github.com/alicelimas/-dsd/blob/main/Atividade%2003%20-%20gRPC/Transmiss%C3%A3o%20de%20Dados%20com%20gRPC.pdf)
