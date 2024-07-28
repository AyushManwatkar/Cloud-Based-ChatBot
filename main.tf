provider "aws" {
  region = "us-east-1"
}

module "dynamodb" {
  source = "./modules/dynamodb"
}

module "iam" {
  source = "./modules/iam"
  dynamodb_table_arn = module.dynamodb.table_arn
}

module "lambda" {
  source = "./modules/lambda"
  lambda_role_arn = module.iam.lambda_role_arn
  depends_on = [module.iam, module.dynamodb]
}

module "lex" {
  source                    = "./modules/lex"
  lambda_function_arns      = module.lambda.lambda_function_arns
  lambda_function_names     = module.lambda.lambda_function_names
  create_lambda_permissions = false
  depends_on                = [module.lambda]
}