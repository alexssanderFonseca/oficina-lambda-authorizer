import requests
import os
from typing import Optional, Dict, Any

# TODO: Substitua esta URL pela URL real do seu serviço de clientes
# Você pode usar uma variável de ambiente para torná-la configurável.
CUSTOMER_API_URL: str = os.environ.get("CUSTOMER_API_URL", "http://api.externa/clientes")

def get_customer_by_cpf(cpf: str) -> Optional[Dict[str, Any]]:
    """
    Busca um cliente pelo CPF em um serviço externo.

    Args:
        cpf: O CPF do cliente a ser buscado.

    Returns:
        Um dicionário com os dados do cliente se encontrado, None caso contrário.
    """
    try:
        response: requests.Response = requests.get(f"{CUSTOMER_API_URL}?cpf={cpf}")

        if response.status_code == 200:
            # Assumindo que a API retorna uma lista de clientes e pegamos o primeiro
            customers: list[Dict[str, Any]] = response.json()
            if customers:
                return customers[0]
            return None
        elif response.status_code == 404:
            return None
        else:
            # Em caso de outros erros do servidor, você pode querer logar o erro
            # e talvez levantar uma exceção.
            response.raise_for_status()
            return None # Adicionado para garantir um retorno em todos os caminhos

    except requests.exceptions.RequestException as e:
        # Logar o erro de conexão aqui seria uma boa prática
        print(f"Erro ao conectar ao serviço de clientes: {e}")
        return None

