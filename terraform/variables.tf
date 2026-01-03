variable "aws_region" {
  description = "The AWS region to deploy resources."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "The name of the project."
  type        = string
  default     = "lambda-authorizer"
}

variable "rds_secret_arn" {
  description = "The ARN of the RDS secret containing database credentials."
  type        = string
}

variable "existing_api_gateway_name" {
  description = "The name of the existing API Gateway to integrate with the Lambda authorizer."
  type        = string
  default = "oficina-api"
}

