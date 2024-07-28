resource "aws_dynamodb_table" "customer_details" {
  name         = "customerdetails"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "accountnumber"

  attribute {
    name = "accountnumber"
    type = "S"
  }
  attribute {
    name = "name"
    type = "S"
  }
  attribute {
    name = "balance"
    type = "N"
  }
  attribute {
    name = "contactnumber"
    type = "S"
  }
  attribute {
    name = "password"
    type = "S"
  }
  attribute {
    name = "last_transaction"
    type = "S"
  }

  global_secondary_index {
    name               = "NameIndex"
    hash_key           = "name"
    projection_type    = "ALL"
  }

  global_secondary_index {
    name               = "BalanceIndex"
    hash_key           = "balance"
    projection_type    = "ALL"
  }

  global_secondary_index {
    name               = "ContactNumberIndex"
    hash_key           = "contactnumber"
    projection_type    = "ALL"
  }

  global_secondary_index {
    name               = "PasswordIndex"
    hash_key           = "password"
    projection_type    = "ALL"
  }
  global_secondary_index {
    name               = "LastTransactionIndex"
    hash_key           = "last_transaction"
    projection_type    = "ALL"
  }
}

output "table_arn" {
  value = aws_dynamodb_table.customer_details.arn
}