import pytest
from unittest.mock import MagicMock, patch
from app.service.customer_service import get_customer_by_cpf

def test_get_customer_by_cpf_success():
    """
    Tests successful retrieval of a customer by CPF.
    """
    cpf = "12345678901"
    db_credentials = {
        "host": "localhost",
        "dbname": "testdb",
        "username": "testuser",
        "password": "testpassword",
        "port": "5432"
    }
    expected_customer = {"id": "1", "nome": "Test", "sobrenome": "User", "cpf_cnpj": cpf}

    with patch('psycopg2.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = expected_customer

        customer = get_customer_by_cpf(cpf, db_credentials)

        mock_connect.assert_called_once_with(
            host="localhost",
            dbname=None, # os.environ.get is not mocked here, so it's None
            user="testuser",
            password="testpassword",
            port="5432"
        )
        mock_cursor.execute.assert_called_once_with(
            "SELECT id, nome, sobrenome, cpf_cnpj FROM cliente WHERE cpf_cnpj = %s", (cpf,)
        )
        assert customer == expected_customer

def test_get_customer_by_cpf_not_found():
    """
    Tests when a customer is not found.
    """
    cpf = "12345678901"
    db_credentials = {
        "host": "localhost",
        "dbname": "testdb",
        "username": "testuser",
        "password": "testpassword",
        "port": "5432"
    }

    with patch('psycopg2.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        customer = get_customer_by_cpf(cpf, db_credentials)

        assert customer is None
