terraform {
  backend "s3" {
    bucket  = "tfstate-fiap-alex-academy-lambda-authorizer"
    key     = "tfstate"                                      
    region  = "us-east-1"
    encrypt = false 
  }
}
