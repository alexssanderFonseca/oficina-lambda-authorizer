output "sam_artifacts_bucket_name" {
  description = "The name of the S3 bucket for storing SAM artifacts."
  value       = aws_s3_bucket.sam_artifacts.bucket
}

output "lambda_exec_role_arn" {
  description = "The ARN of the IAM role for the Lambda function."
  value       = aws_iam_role.lambda_exec_role.arn
}