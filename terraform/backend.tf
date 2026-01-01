terraform {
  backend "s3" {
    bucket  = "tfstate-fiap-alex-academy-lambda-authorizer" # Novo bucket para este projeto
    key     = "tfstate"                                      # Chave padrão
    region  = "us-east-1"
    encrypt = false # Para consistência com o outro projeto, mas true é recomendado
  }
}
