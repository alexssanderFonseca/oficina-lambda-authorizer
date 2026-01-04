import os
import boto3
import json
from typing import Dict, Any
from aws_lambda_powertools import Logger

logger: Logger = Logger()

# Cache para armazenar o segredo após a primeira recuperação
_cached_secret: Dict[str, Any] = {}

def get_secret(secret_name: str) -> Dict[str, Any]:
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
