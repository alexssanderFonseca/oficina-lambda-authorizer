data "aws_vpc" "selected" {
  cidr_block = "10.0.0.0/16"
}


data "aws_subnets" "all" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.selected.id]
  }
}

data "aws_subnet" "details" {
  for_each = toset(data.aws_subnets.all.ids)
  id       = each.value
}

data "aws_secretsmanager_secret" "rds_credentials" {
  arn = "arn:aws:secretsmanager:us-east-1:305448253775:secret:secrets-XmZ0Fb"
}