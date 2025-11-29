import json
import uuid
from typing import Any, Dict
from pytest_mock import MockerFixture
from app import app

def lambda_context() -> object:
    class LambdaContext:
        def __init__(self) -> None:
            self.function_name: str = "test-func"
            self.memory_limit_in_mb: int = 128
            self.invoked_function_arn: str = "arn:aws:lambda:eu-west-1:809313241234:function:test-func"
            self.aws_request_id: str = "52fdfc07-2182-154f-163f-5f0f9a621d72"

        def get_remaining_time_in_millis(self) -> int:
            return 1000

    return LambdaContext()

def test_generate_token_success_for_existing_customer(apigw_event_post_cpf: Dict[str, Any], mocker: MockerFixture) -> None:
    """
    Tests if a token is generated successfully for an existing customer.
    """
    mock_user_id: str = str(uuid.uuid4())
    mock_customer: Dict[str, Any] = {"id": mock_user_id, "name": "Test User", "cpf": "12345678909"}
    
    # Mock the external service call
    mock_get_customer = mocker.patch("app.app.get_customer_by_cpf", return_value=mock_customer)
    
    # Mock the JWT generation
    mock_generate_jwt = mocker.patch("app.app.generate_jwt", return_value="mock_token")
    
    ret: Dict[str, Any] = app.lambda_handler(apigw_event_post_cpf, lambda_context())
    
    assert ret["statusCode"] == 200
    assert json.loads(ret["body"]) == {"token": "mock_token"}
    
    # Verify that get_customer_by_cpf was called with the correct CPF
    mock_get_customer.assert_called_once_with("12345678909")
    
    # Verify that generate_jwt was called with the correct user ID
    mock_generate_jwt.assert_called_once_with(mock_user_id)


def test_generate_token_returns_404_for_non_existing_customer(apigw_event_post_cpf: Dict[str, Any], mocker: MockerFixture) -> None:
    """
    Tests if a 404 is returned for a non-existing customer.
    """
    # Mock the external service call to return None (customer not found)
    mock_get_customer = mocker.patch("app.app.get_customer_by_cpf", return_value=None)
    
    ret: Dict[str, Any] = app.lambda_handler(apigw_event_post_cpf, lambda_context())
    
    assert ret["statusCode"] == 404
    assert json.loads(ret["body"]) == {"message": "Cliente não encontrado"}
    mock_get_customer.assert_called_once_with("12345678909")


def test_generate_token_returns_400_if_cpf_is_missing(mocker: MockerFixture) -> None:
    """
    Tests if a 400 is returned if the CPF is not in the request body.
    """
    # Create an event with an empty body and necessary keys for powertools
    event: Dict[str, Any] = {
        "body": json.dumps({}),
        "httpMethod": "POST",
        "path": "/",
        "headers": {"Content-Type": "application/json"},
        "requestContext": {"httpMethod": "POST", "path": "/"},
    }
    
    ret: Dict[str, Any] = app.lambda_handler(event, lambda_context())
    
    assert ret["statusCode"] == 400
    assert json.loads(ret["body"]) == {"message": "CPF não informado"}
