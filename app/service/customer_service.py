import os
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional, Dict, Any

from aws_lambda_powertools import Logger

logger: Logger = Logger()



def get_customer_by_cpf(cpf: str, db_credentials: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Busca um cliente pelo CPF diretamente no banco de dados.

    Args:
        cpf: O CPF do cliente a ser buscado.
        db_credentials: As credenciais para conexão com o banco de dados.

    Returns:
        Um dicionário com os dados do cliente se encontrado, None caso contrário.
    """
    conn = None
    try:
        conn = psycopg2.connect(
            host=db_credentials.get("host"),
            dbname=os.environ.get("DB_NAME"),
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