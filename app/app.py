import json
from typing import Dict, Any, Optional
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer
from aws_lambda_powertools import Metrics

from service.customer_service import get_customer_by_cpf
from service.jwt_generator import generate_jwt

tracer = Tracer()
logger = Logger()
metrics = Metrics(namespace="Powertools")

def _build_response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    """Helper to build API Gateway proxy response."""
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    }

@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    try:
        request_body: Dict[str, Any] = json.loads(event.get("body", "{}"))
        cpf: Optional[str] = request_body.get('cpf')

        if not cpf:
            logger.warning("CPF not provided in request body")
            return _build_response(400, {"message": "CPF não informado"})

        customer: Optional[Dict[str, Any]] = get_customer_by_cpf(cpf)

        if customer and customer.get('id'):
            user_id: str = customer['id']
            logger.info(f"Customer found for CPF. Generating token for user ID: {user_id}")
            token: str = generate_jwt(user_id)
            return _build_response(200, {"token": token})
        else:
            logger.info(f"Customer not found for CPF: {cpf}")
            return _build_response(404, {"message": "Cliente não encontrado"})
            
    except json.JSONDecodeError as e:
        logger.exception("Failed to decode JSON from request body")
        return _build_response(400, {"message": f"Invalid JSON format: {e}"})
    except Exception as e:
        logger.exception("An unexpected error occurred")
        return _build_response(500, {"message": "Internal server error"})
