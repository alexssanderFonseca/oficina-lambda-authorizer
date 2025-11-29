# 🛡️ lambda-authorizer

Este projeto implementa um Autorizador AWS Lambda utilizando Python e o AWS Serverless Application Model (SAM). Ele provê um endpoint no API Gateway que valida um CPF (Cadastro de Pessoas Físicas) através de um serviço externo e, em caso de validação bem-sucedida, gera um JSON Web Token (JWT) contendo um ID de usuário único. Este token pode então ser usado para autorizar requisições subsequentes a outros serviços.

A aplicação utiliza o [**AWS Lambda Powertools for Python**](https://awslabs.github.io/aws-lambda-powertools-python/latest/) para as melhores práticas de desenvolvimento serverless, incluindo logging estruturado, rastreamento (tracing) e métricas personalizadas.

## ✨ Funcionalidades

*   **Validação Segura de CPF**: 🎯 Recebe um CPF via requisição POST e valida sua existência e autenticidade chamando um serviço externo de clientes.
*   **Geração de JWT**: 🔑 Após a validação bem-sucedida, gera um JWT assinado com uma chave secreta. O payload do JWT inclui um ID de usuário único não sensível (`sub` claim), garantindo que informações pessoais sensíveis (como o CPF) não sejam expostas diretamente no token.
*   **Tratamento Robusto de Erros**:
    *   Retorna `400 Bad Request` (Requisição Inválida) se o CPF não for fornecido na requisição.
    *   Retorna `404 Not Found` (Não Encontrado) se o serviço externo de clientes não encontrar um cliente associado ao CPF fornecido.
*   **Observabilidade com AWS Lambda Powertools**: 📊 Integra Logging, Tracing e Métricas para fornecer insights aprofundados sobre a operação da função Lambda.
*   **Tipagem Estrita (Type Hinting)**: 📝 O código-fonte é totalmente tipado, melhorando a legibilidade, manutenibilidade e permitindo a análise estática.
*   **Testes Unitários**: ✅ Testes unitários abrangentes usando `pytest` e `pytest-mock` garantem a confiabilidade da lógica da aplicação.

## 📁 Estrutura do Projeto

*   `app/`: Contém a função Lambda principal (`app.py`) e suas dependências específicas (`requirements.txt`).
*   `service/`: Abriga módulos de lógica de negócios, incluindo `customer_service.py` (para chamadas à API externa de clientes) e `jwt_generator.py` (para criação de JWT).
*   `events/`: Exemplos de eventos de invocação para testes locais.
*   `tests/`: Testes unitários e de integração para a aplicação.
    *   `tests/unit/test_handler.py`: Contém testes unitários para o handler principal da Lambda.
    *   `tests/conftest.py`: Define fixtures do `pytest` para simular eventos do API Gateway.
*   `template.yaml`: Define os recursos AWS da aplicação usando AWS SAM.

## 💻 Desenvolvimento Local e Testes

### Pré-requisitos

*   [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
*   [Python 3.12](https://www.python.org/downloads/)
*   [Docker](https://hub.docker.com/search/?type=edition&offering=community)
*   Um ambiente virtual (ex: `python3.12 -m venv .venv`)

### Configuração

1.  **Ativar Ambiente Virtual**:
    ```bash
    source .venv/bin/activate
    ```
2.  **Instalar Dependências**:
    ```bash
    pip install -r app/requirements.txt
    pip install -r tests/requirements.txt
    ```
3.  **Configurar URL do Serviço Externo de Clientes**:
    O módulo `service/customer_service.py` faz chamadas a uma API externa. Configure sua URL usando uma variável de ambiente. Para testes locais, você pode exportá-la em seu shell:
    ```bash
    export CUSTOMER_API_URL="http://sua-api-externa-de-clientes.com/clientes"
    # Exemplo: export CUSTOMER_API_URL="http://localhost:8080/clientes" se estiver rodando uma API mock local
    ```

### Executando Testes Unitários

Para executar os testes unitários:

```bash
pytest tests/unit -v
```

### Executando a Aplicação Localmente

O SAM CLI pode emular a API da sua aplicação localmente.

1.  **Construa sua aplicação**:
    ```bash
    sam build --use-container
    ```
2.  **Inicie o API Gateway local**:
    ```bash
    sam local start-api
    ```
    Isso geralmente tornará a API disponível em `http://127.0.0.1:3000`.

3.  **Invoque a API**:

    *   **POST / (Gerar Token - Sucesso)**: 🚀
        ```bash
        curl -X POST -H "Content-Type: application/json" -d '{"cpf": "12345678909"}' http://127.0.0.1:3000/
        ```
        (Substitua `12345678909` por um CPF que sua `CUSTOMER_API_URL` mockada retornaria um cliente).

    *   **POST / (Gerar Token - Cliente Não Encontrado)**: 🕵️‍♀️
        ```bash
        curl -X POST -H "Content-Type: application/json" -d '{"cpf": "99988877766"}' http://127.0.0.1:3000/
        ```
        (Substitua `99988877766` por um CPF que sua `CUSTOMER_API_URL` mockada retornaria 404).

    *   **POST / (Gerar Token - CPF Ausente)**: 🚫
        ```bash
        curl -X POST -H "Content-Type: application/json" -d '{}' http://127.0.0.1:3000/
        ```

    *   **GET /hello**: 👋
        ```bash
        curl http://127.0.0.1:3000/hello
        ```

## 🚀 Deployment

Para fazer o deploy da sua aplicação na AWS, siga o processo padrão de deploy do SAM CLI:

```bash
sam deploy --guided
```

Siga as instruções para configurar seu deploy (Nome da Stack, Região AWS, etc.).

## 🧹 Limpeza

Para deletar os recursos AWS que foram deployados:

```bash
sam delete --stack-name "nome-da-sua-stack"
```

## 📚 Recursos Adicionais

Consulte o [guia do desenvolvedor AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) para uma introdução à especificação SAM, o SAM CLI e conceitos de aplicações serverless.
