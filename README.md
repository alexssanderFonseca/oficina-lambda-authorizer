# 🛡️ lambda-authorizer

Este projeto implementa um Autorizador AWS Lambda utilizando Python e Terraform. Ele provê um endpoint no API Gateway que valida um CPF (Cadastro de Pessoas Físicas) através de um serviço externo e, em caso de validação bem-sucedida, gera um JSON Web Token (JWT) contendo um ID de usuário único. Este token pode então ser usado para autorizar requisições subsequentes a outros serviços.

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
*   `terraform/`: Define a infraestrutura como código usando Terraform.

## 💻 Desenvolvimento Local e Testes

### Pré-requisitos

*   [Terraform CLI](https://learn.hashicorp.com/tutorials/terraform/install-cli)
*   [Python 3.12](https://www.python.org/downloads/)
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

## 🚀 Deployment

Para fazer o deploy da sua aplicação na AWS, siga o processo padrão de deploy do Terraform:

1.  **Navegue até o diretório do Terraform**:
    ```bash
    cd terraform
    ```
2.  **Inicialize o Terraform**:
    ```bash
    terraform init
    ```
3.  **Planeje as alterações**:
    ```bash
    terraform plan
    ```
4.  **Aplique as alterações**:
    ```bash
    terraform apply
    ```

Siga as instruções para configurar seu deploy.

## 🧹 Limpeza

Para deletar os recursos AWS que foram deployados:

```bash
cd terraform
terraform destroy
```

## 📚 Recursos Adicionais

Consulte a [documentação do Terraform](https://www.terraform.io/docs) para mais informações sobre como gerenciar sua infraestrutura como código.
