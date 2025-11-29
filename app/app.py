from typing import Tuple, Dict, Any, Optional
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer
from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit

from service.customer_service import get_customer_by_cpf
from service.jwt_generator import generate_jwt

app: APIGatewayRestResolver = APIGatewayRestResolver()
tracer: Tracer = Tracer()
logger: Logger = Logger()
metrics: Metrics = Metrics(namespace="Powertools")

@app.post("/") 
@tracer.capture_method
def generate_token() -> Tuple[Dict[str, str], int]:
    request_body: Dict[str, Any] = app.current_event.json_body
    cpf: Optional[str] = request_body.get('cpf')

    if not cpf:
        logger.warning("CPF not provided in request body")
        return {"message": "CPF não informado"}, 400

    customer: Optional[Dict[str, Any]] = get_customer_by_cpf(cpf)

    if customer and customer.get('id'):
        user_id: str = customer['id']
        logger.info(f"Customer found for CPF. Generating token for user ID: {user_id}")
        token: str = generate_jwt(user_id)
        return {"token": token}, 200
    else:
        logger.info(f"Customer not found for CPF: {cpf}")
        return {"message": "Cliente não encontrado"}, 404

@app.get("/hello")
@tracer.capture_method
def hello() -> Dict[str, str]:
    # adding custom metrics
    # See: https://awslabs.github.io/aws-lambda-powertools-python/latest/core/metrics/
    metrics.add_metric(name="HelloWorldInvocations", unit=MetricUnit.Count, value=1)

    # structured log
    # See: https://awslabs.github.io/aws-lambda-powertools-python/latest/core/logger/
    logger.info("Hello world API - HTTP 200")
    return {"message": "hello world"}

# Enrich logging with contextual information from Lambda
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
# Adding tracer
# See: https://awslabs.github.io/aws-lambda-powertools-python/latest/core/tracer/
@tracer.capture_lambda_handler
# ensures metrics are flushed upon request completion/failure and capturing ColdStart metric
@metrics.log_metrics(capture_cold_start_metric=True)
def lambda_handler(event: Dict[str, Any], context: LambdaContext) -> Dict[str, Any]:
    return app.resolve(event, context)
