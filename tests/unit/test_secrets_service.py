import pytest
from unittest.mock import MagicMock, patch
import importlib
from app.service import secrets_service

@pytest.fixture(autouse=True)
def reload_module():
    importlib.reload(secrets_service)

def test_get_secret_success():
    """
    Tests successful retrieval of a secret from AWS Secrets Manager.
    """
    secret_name = "test_secret"
    secret_value = {"username": "test_user", "password": "test_password"}
    

    # Mock the boto3 client and its methods
    mock_boto3_client = MagicMock()
    mock_boto3_client.get_secret_value.return_value = {
        'SecretString': '{"username": "test_user", "password": "test_password"}'
    }
    
    with patch('boto3.client', return_value=mock_boto3_client) as mock_boto3:
        # First call, should call boto3
        result = secrets_service.get_secret(secret_name)
        assert result == secret_value
        mock_boto3.assert_called_once_with('secretsmanager')
        mock_boto3_client.get_secret_value.assert_called_once_with(SecretId=secret_name)

        # Second call, should use cache
        result2 = secrets_service.get_secret(secret_name)
        assert result2 == secret_value
        # Assert that boto3 client was not called again
        mock_boto3.assert_called_once()
        mock_boto3_client.get_secret_value.assert_called_once()


def test_get_secret_raises_exception():
    """
    Tests that an exception is raised when the secret cannot be retrieved.
    """
    secret_name = "non_existent_secret"
    
    mock_boto3_client = MagicMock()
    mock_boto3_client.get_secret_value.side_effect = Exception("Secret not found")
    
    with patch('boto3.client', return_value=mock_boto3_client):
        with pytest.raises(Exception, match="Secret not found"):
            secrets_service.get_secret(secret_name)
