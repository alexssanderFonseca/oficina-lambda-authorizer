import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, Dict, Any
import boto3
import json

from aws_lambda_powertools import Logger

logger: Logger = Logger()



def get_customer_by_cpf(cpf: str) -> Optional[Dict[str, Any]]:
    """
    Busca um cliente pelo CPF diretamente no banco de dados.

    Args:
        cpf: O CPF do cliente a ser buscado.

    Returns:
        Um dicionário com os dados do cliente se encontrado, None caso contrário.
    """
    conn = None
    try:
        secret_name = os.environ.get("SECRET_NAME")
        if not secret_name:
            raise ValueError("SECRET_NAME environment variable not set.")

        db_credentials = get_secret(secret_name)

        # Conexão com o banco de dados usando credenciais do Secrets Manager
        conn = psycopg2.connect(
            host=db_credentials.get("host"),
            dbname=os.environ.get("DB_NAME"), # DB_NAME ainda pode vir do ambiente, se for diferente por stage
            user=db_credentials.get("username"),
            password=db_credentials.get("password"),
            port=db_credentials.get("port", "5432")
        )
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, nome, sobrenome, cpf_cnpj FROM cliente WHERE cpf_cnpj = %s", (cpf,))
            customer = cur.fetchone()
            return customer

    except psycopg2.Error as e:
        logger.error(f"Erro no banco de dados: {e}")
        return None
    except ValueError as e:
        logger.error(f"Erro de configuração ou segredo: {e}")
        return None
    finally:
        if conn:
            conn.close()

# Cache para armazenar o segredo após a primeira recuperação
_cached_secret = None

def get_secret(secret_name: str) -> Dict[str, str]:
    """
    Recupera o segredo do AWS Secrets Manager.
    Armazena em cache para evitar chamadas repetidas à API.
    """
    global _cached_secret
    if _cached_secret:
        return _cached_secret

    try:
        client = boto3.client('secretsmanager')
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            _cached_secret = json.loads(secret)
            return _cached_secret
        else:
            # Secrets binários não são esperados aqui para credenciais de DB
            raise ValueError("Secret not found or not a string secret.")
    except Exception as e:
        logger.error(f"Erro ao recuperar o segredo '{secret_name}' do Secrets Manager: {e}")
        raise