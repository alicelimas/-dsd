# Sistema de Fila de Mensagens com RabbitMQ e API Gateway

Este projeto implementa um sistema básico de filas de mensagens usando o **RabbitMQ** como Message-Oriented Middleware (MOM), com processos produtores e consumidores. Um API Gateway foi criado para enviar mensagens para o RabbitMQ, e consumidores processam essas mensagens.

## Estrutura do Projeto

- `api_gateway.py`: contém a lógica do produtor. Define uma API Flask com uma rota /rabbitmq que aceita POST e publica mensagens na fila minha_fila.
- `consumidor.py`: contém a lógica do consumidor. Conecta-se ao RabbitMQ, consome mensagens da fila minha_fila e as imprime no console.

## Tecnologias Utilizadas

- **Python**: linguagem utilizada para a implementação do consumidor e do api_gateway.
- **Flask**: framework web para criar a API do produtor.
- **RabbitMQ**: para gerenciamento de filas de mensagens.
- **Pika**: biblioteca Python para interação com o RabbitMQ.

## Requisitos

- **Python** (versão 3.6 ou superior)
- **Docker** (para rodar o RabbitMQ) ou RabbitMQ instalado localmente.
- **Bibliotecas Python**:
  - `pika`
  - `flask`

## Instalação

1. **Clonar o Repositório**

    Antes de tudo, certifique-se de estar no diretório de Atividade 05 - mom.

    cd . -dsd\Atividade 05 - mom\

2. **Criação e ativação de ambiente virtual**
    ```
    python -m venv venv
    ```
    Para ativá-la, rodamos o seguinte comando:
    ```
    venv\Scripts\activate
    ```
3. **Instalação das dependências do Python**
    1. Você pode simplesmente instalar a partir do arquivo de requirements.txt, através do seguinte comando:
    ```
    pip install -r requirements.txt
    ```
    2. Ou, se preferir, pode instalar manualmente, executando o seguinte comando:
    ```
    pip install pika flask
    ```
    Para verificar se as bibiliotecas foram instaladas corretamente, execute:
    ```
    pip list 
    ```
4. **Verifique se o RabbitMQ está rodando**
    O serviço costuma ser iniciado automaticamente após a instalação. Ou use o seguinte comando no terminal, se instalado manualmente:
    ```
    rabbitmq-server
    ```
    Isso iniciará o RabbitMQ e a interface de administração estará disponível em http://localhost:15672. As credenciais padrão são:

    Usuário: guest

    Senha: guest

    Utilize-as.

5. **Rode o Consumidor**
    Abra um outro terminal, ative a venv e rode o seguinte comando:
    ```
    python consumidor.py
    ```
    **A saída esperada é: "Aguardando mensagens. Pressione CTRL+C para sair."**

6. **Rode o Produtor**
    Abra um outro terminal, ative a venv também e rode o seguinte comando:
    ```
    python api_gateway.py
    ```
    **A saída esperada é: "Running on http://localhost:5000".**


7. **Envie Mensagens para o RabbitMQ**
    Em um outro terminal, envie uma requisição POST. Caso esteja utilizando o VSCode/PowerShell, use o seguinte comando:
    ```
    Invoke-WebRequest -Uri "http://localhost:5000/rabbitmq" -Method POST -Headers @{"Content-Type" = "application/json"} -Body '{"message": "Olá!"}'
    ```
    Na saída do consumidor, aparecerá: **Mensagem recebida: Olá!**

    Caso possua curl instalado:
    ```
    curl -X POST http://localhost:5000/rabbitmq -H "Content-Type: application/json" -d "{\"message\": \"Teste do sistema\"}"
    ```
    Na saída do consumidor, aparecerá: **Mensagem recebida: Mensagem de Teste!**