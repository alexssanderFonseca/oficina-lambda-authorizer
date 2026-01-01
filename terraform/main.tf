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
  block_public_and_cross_account_access = true
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
