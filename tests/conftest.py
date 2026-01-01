import pytest
import json
from typing import Dict, Any

@pytest.fixture
def apigw_event_post_cpf() -> Dict[str, Any]:
    """ Generates API GW Event for POST with a valid CPF number."""
    return {
        "body": json.dumps({"cpf": "12345678909"}),
        "headers": {
            "Content-Type": "application/json"
        },
        "httpMethod": "POST",
        "isBase64Encoded": False,
        "path": "/",
        "requestContext": {
            "resourcePath": "/",
            "httpMethod": "POST",
            "protocol": "HTTP/1.1",
        },
        "resource": "/",
    }
