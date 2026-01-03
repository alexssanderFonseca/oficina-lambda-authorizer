data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "sam_artifacts" {
  bucket = "${var.project_name}-sam-artifacts-${data.aws_caller_identity.current.account_id}"

  tags = {
    Name = "${var.project_name}-sam-artifacts"
  }
}

resource "aws_s3_bucket_versioning" "sam_artifacts_versioning" {
  bucket = aws_s3_bucket.sam_artifacts.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "sam_artifacts_block_public_access" {
  bucket                  = aws_s3_bucket.sam_artifacts.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "${var.project_name}-lambda-exec-role"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Action    = "sts:AssumeRole",
        Effect    = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "${var.project_name}-lambda-exec-role"
  }
}

resource "aws_iam_role_policy_attachment" "lambda_vpc_access" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_iam_policy" "secrets_manager_policy" {
  name        = "${var.project_name}-secrets-manager-policy"
  description = "Policy to allow access to specific secrets in AWS Secrets Manager"

  policy = jsonencode({
    Version   = "2012-10-17",
    Statement = [
      {
        Action = [
          "secretsmanager:GetSecretValue"
        ],
        Effect   = "Allow",
        Resource = var.rds_secret_arn # Usando o ARN do secret do projeto RDS, passado como variável
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "secrets_manager_access" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.secrets_manager_policy.arn
}

# Upload Lambda package to S3
resource "aws_s3_object" "lambda_package" {
  bucket = aws_s3_bucket.sam_artifacts.id
  key    = "lambda-${filemd5(var.lambda_zip_path)}.zip"
  source = var.lambda_zip_path
}

# Lambda Function
resource "aws_lambda_function" "authorizer" {
  function_name = "${var.project_name}-function"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "app.lambda_handler"
  runtime       = "python3.12"
  s3_bucket     = aws_s3_object.lambda_package.bucket
  s3_key        = aws_s3_object.lambda_package.key
  source_code_hash = filebase64sha256(var.lambda_zip_path)

  environment {
    variables = {
      SECRET_NAME = "rds-academico-credentials-1"
      DBName      = "db_staging" # Adjust as needed, or create a map
    }
  }

  tags = {
    Name = "${var.project_name}-function"
  }
}

# API Gateway Integration
data "aws_api_gateway_rest_api" "existing_api" {
  id = var.existing_api_gateway_id
}

resource "aws_api_gateway_resource" "clientes" {
  rest_api_id = data.aws_api_gateway_rest_api.existing_api.id
  parent_id   = data.aws_api_gateway_rest_api.existing_api.root_resource_id
  path_part   = "clientes"
}

resource "aws_api_gateway_resource" "login" {
  rest_api_id = data.aws_api_gateway_rest_api.existing_api.id
  parent_id   = aws_api_gateway_resource.clientes.id
  path_part   = "login"
}

resource "aws_api_gateway_method" "post" {
  rest_api_id   = data.aws_api_gateway_rest_api.existing_api.id
  resource_id   = aws_api_gateway_resource.login.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id             = data.aws_api_gateway_rest_api.existing_api.id
  resource_id             = aws_api_gateway_resource.login.id
  http_method             = aws_api_gateway_method.post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.authorizer.invoke_arn
}

resource "aws_lambda_permission" "apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.authorizer.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${data.aws_api_gateway_rest_api.existing_api.execution_arn}/*/${aws_api_gateway_method.post.http_method}${aws_api_gateway_resource.login.path}"
}

resource "aws_api_gateway_deployment" "deploy" {
  rest_api_id = data.aws_api_gateway_rest_api.existing_api.id
  
  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.login.id,
      aws_api_gateway_method.post.id,
      aws_api_gateway_integration.lambda.id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}
