# Lambda Functions

variable "lambda_role_arn" {
  description = "ARN of the IAM role for Lambda functions"
  type        = string
}

resource "aws_lambda_function" "create_account" {
  function_name = "create_account"
  handler       = "create_account.lambda_handler"
  runtime       = "python3.8"
  filename      = "${path.module}/../../zip_files/create_account.zip"
  role          = var.lambda_role_arn
}

resource "aws_lambda_permission" "allow_lex_create_account" {
  statement_id  = "AllowLexInvokeCreateAccount"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.create_account.function_name
  principal     = "lex.amazonaws.com"
}

resource "aws_lambda_function" "delete_account" {
  function_name = "delete_account"
  handler       = "delete_account.lambda_handler"
  runtime       = "python3.8"
  filename      = "${path.module}/../../zip_files/delete_account.zip"
  role          = var.lambda_role_arn
}

resource "aws_lambda_permission" "allow_lex_delete_account" {
  statement_id  = "AllowLexInvokeDeleteAccount"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.delete_account.function_name
  principal     = "lex.amazonaws.com"
}

resource "aws_lambda_function" "fund_transfer" {
  function_name = "fund_transfer"
  handler       = "fund_transfer.lambda_handler"
  runtime       = "python3.8"
  filename      = "${path.module}/../../zip_files/fund_transfer.zip"
  role          = var.lambda_role_arn
}

resource "aws_lambda_permission" "allow_lex_fund_transfer" {
  statement_id  = "AllowLexInvokeFundTransfer"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.fund_transfer.function_name
  principal     = "lex.amazonaws.com"
}

resource "aws_lambda_function" "withdraw" {
  function_name = "withdraw"
  handler       = "withdraw.lambda_handler"
  runtime       = "python3.8"
  filename      = "${path.module}/../../zip_files/withdraw.zip"
  role          = var.lambda_role_arn
}

resource "aws_lambda_permission" "allow_lex_withdraw" {
  statement_id  = "AllowLexInvokeWithdraw"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.withdraw.function_name
  principal     = "lex.amazonaws.com"
}

resource "aws_lambda_function" "balance_enquiry" {
  function_name = "balance_enquiry"
  handler       = "balance_enquiry.lambda_handler"
  runtime       = "python3.8"
  filename      = "${path.module}/../../zip_files/balance_enquiry.zip"
  role          = var.lambda_role_arn
}

resource "aws_lambda_permission" "allow_lex_balance_enquiry" {
  statement_id  = "AllowLexInvokeBalanceEnquiry"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.balance_enquiry.function_name
  principal     = "lex.amazonaws.com"
}

resource "aws_lambda_function" "last_transaction" {
  function_name = "last_transaction"
  handler       = "last_transaction.lambda_handler"
  runtime       = "python3.8"
  filename      = "${path.module}/../../zip_files/last_transaction.zip"
  role          = var.lambda_role_arn
}

resource "aws_lambda_permission" "allow_lex_last_transaction" {
  statement_id  = "AllowLexInvokeLastTransaction"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.last_transaction.function_name
  principal     = "lex.amazonaws.com"
}

output "lambda_function_arns" {
  value = {
    create_account   = aws_lambda_function.create_account.arn
    delete_account   = aws_lambda_function.delete_account.arn
    fund_transfer    = aws_lambda_function.fund_transfer.arn
    withdraw         = aws_lambda_function.withdraw.arn
    balance_enquiry  = aws_lambda_function.balance_enquiry.arn
    last_transaction = aws_lambda_function.last_transaction.arn
  }
}

output "lambda_function_names" {
  value = {
    create_account   = aws_lambda_function.create_account.function_name
    delete_account   = aws_lambda_function.delete_account.function_name
    fund_transfer    = aws_lambda_function.fund_transfer.function_name
    withdraw         = aws_lambda_function.withdraw.function_name
    balance_enquiry  = aws_lambda_function.balance_enquiry.function_name
    last_transaction = aws_lambda_function.last_transaction.function_name
  }
}