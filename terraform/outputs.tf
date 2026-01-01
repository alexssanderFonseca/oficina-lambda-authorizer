output "sam_artifacts_bucket_name" {
  description = "Name of the S3 bucket for SAM artifacts"
  value       = aws_s3_bucket.sam_artifacts.bucket
}

output "lambda_exec_role_arn" {
  description = "ARN of the Lambda execution IAM role"
  value       = aws_iam_role.lambda_exec_role.arn
}
