variable "aws_region" {
  description = "The AWS region to deploy resources."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "The name of the project."
  type        = string
  default     = "lambda-oficina-authorizer"
}

variable "rds_secret_arn" {
  description = "The ARN of the RDS secret containing database credentials."
  type        = string
  default     = "arn:aws:secretsmanager:us-east-1:305448253775:secret:secrets-XmZ0Fb"
}

variable "existing_api_gateway_name" {
  description = "The name of the existing API Gateway to integrate with the Lambda authorizer."
  type        = string
  default     = "oficina-api"
}

variable "lambda_zip_path" {
  description = "The path to the Lambda function's deployment package (zip file)."
  type        = string
}
