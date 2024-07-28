# Lex Intents

variable "lambda_function_arns" {
  description = "ARNs of the Lambda functions"
  type        = map(string)
}

variable "lambda_function_names" {
  description = "Names of the Lambda functions"
  type        = map(string)
}

variable "create_lambda_permissions" {
  description = "Whether to create Lambda permissions"
  type        = bool
  default = false
}

resource "aws_lambda_permission" "allow_lex_create_account" {
    count         = var.create_lambda_permissions ? 1 : 0
  statement_id  = "AllowLexInvokeCreateAccount"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_names["create_account"]
  principal     = "lex.amazonaws.com"
}

resource "aws_lambda_permission" "allow_lex_delete_account" {
    count         = var.create_lambda_permissions ? 1 : 0
  statement_id  = "AllowLexInvokeDeleteAccount"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_names["delete_account"]
  principal     = "lex.amazonaws.com"
}

resource "aws_lambda_permission" "allow_lex_fund_transfer" {
    count         = var.create_lambda_permissions ? 1 : 0
  statement_id  = "AllowLexInvokeFundTransfer"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_names["fund_transfer"]
  principal     = "lex.amazonaws.com"
}

resource "aws_lambda_permission" "allow_lex_withdraw" {
    count         = var.create_lambda_permissions ? 1 : 0
  statement_id  = "AllowLexInvokeWithdraw"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_names["withdraw"]
  principal     = "lex.amazonaws.com"
}

resource "aws_lambda_permission" "allow_lex_balance_enquiry" {
    count         = var.create_lambda_permissions ? 1 : 0
  statement_id  = "AllowLexInvokeBalanceEnquiry"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_names["balance_enquiry"]
  principal     = "lex.amazonaws.com"
}

resource "aws_lambda_permission" "allow_lex_last_transaction" {
    count         = var.create_lambda_permissions ? 1 : 0
  statement_id  = "AllowLexInvokeLastTransaction"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_names["last_transaction"]
  principal     = "lex.amazonaws.com"
}

resource "aws_lex_intent" "create_account" {
  name        = "CreateAccount"
  description = "Intent to create a new account"
  sample_utterances = [
    "Create an account",
    "I want to open a new account",
  ]

  slot {
    name             = "Name"
    description      = "The name of the account holder"
    slot_constraint  = "Required"
    slot_type        = "AMAZON.Person"
    priority = 1
    value_elicitation_prompt {
      max_attempts = 2
      message {
        content_type = "PlainText"
        content      = "What is your name?"
      }
    }
  }

  slot {
    name             = "CreditAmount"
    description      = "The initial deposit amount"
    slot_constraint  = "Required"
    slot_type        = "AMAZON.NUMBER"
    priority = 3
    value_elicitation_prompt {
      max_attempts = 2
      message {
        content_type = "PlainText"
        content      = "How much would you like to deposit?"
      }
    }
  }

  slot {
    name             = "ContactNumber"
    description      = "The contact number of the account holder"
    slot_constraint  = "Required"
    slot_type        = "AMAZON.PhoneNumber"
    priority = 2
    value_elicitation_prompt {
      max_attempts = 2
      message {
        content_type = "PlainText"
        content      = "What is your contact number?"
      }
    }
  }

  fulfillment_activity {
    type = "CodeHook"
    code_hook {
      message_version = "1.0"
      uri             = var.lambda_function_arns["create_account"]
    }
  }
  #depends_on = [aws_lambda_permission.allow_lex_create_account]
}

resource "aws_lex_intent" "delete_account" {
  name        = "DeleteAccount"
  description = "Intent to delete an account"
  sample_utterances = [
    "Delete my account",
    "I want to close my account",
  ]

  slot {
    name             = "AccountNumber"
    description      = "The account number of the account holder"
    slot_constraint  = "Required"
    slot_type        = "AMAZON.NUMBER"
    priority = 1
    value_elicitation_prompt {
      max_attempts = 2
      message {
        content_type = "PlainText"
        content      = "What is your account number?"
      }
    }
  }

  slot {
    name             = "Password"
    description      = "Password for authentication"
    slot_constraint  = "Required"
    slot_type        = "AMAZON.AlphaNumeric"
    priority = 2
    value_elicitation_prompt {
      max_attempts = 2
      message {
        content_type = "PlainText"
        content      = "Please provide your password for verification."
      }
    }
  }

  fulfillment_activity {
    type = "CodeHook"
    code_hook {
      message_version = "1.0"
      uri             = var.lambda_function_arns["delete_account"]
    }
  }
  #depends_on = [aws_lambda_permission.allow_lex_delete_account]
}

resource "aws_lex_intent" "fund_transfer" {
  name        = "FundTransfer"
  description = "Intent to transfer funds"
  sample_utterances = [
    "Transfer money",
    "I want to move funds",
  ]

  slot {
    name             = "Senderacc"
    description      = "Sender Account Number"
    slot_constraint  = "Required"
    slot_type        = "AMAZON.NUMBER"
    priority = 1
    value_elicitation_prompt {
      max_attempts = 2
      message {
        content_type = "PlainText"
        content      = "What is sender account number?"
      }
    }
  }

  slot {
    name             = "Receiveracc"
    description      = "Receiver Account Number"
    slot_constraint  = "Required"
    slot_type        = "AMAZON.NUMBER"
    priority = 4
    value_elicitation_prompt {
      max_attempts = 2
      message {
        content_type = "PlainText"
        content      = "What is receiver account number?"
      }
    }
  }

  slot {
    name             = "Amount"
    description      = "Amount to transfer"
    slot_constraint  = "Required"
    slot_type        = "AMAZON.NUMBER"
    priority = 3
    value_elicitation_prompt {
      max_attempts = 2
      message {
        content_type = "PlainText"
        content      = "How much money would you like to transfer?"
      }
    }
  }

  slot {
    name             = "Password"
    description      = "Password for authentication"
    slot_constraint  = "Required"
    slot_type        = "AMAZON.AlphaNumeric"
    priority = 2
    value_elicitation_prompt {
      max_attempts = 2
      message {
        content_type = "PlainText"
        content      = "Please provide your password for verification."
      }
    }
  }

  fulfillment_activity {
    type = "CodeHook"
    code_hook {
      message_version = "1.0"
      uri             = var.lambda_function_arns["fund_transfer"]
    }
  }
  #depends_on = [aws_lambda_permission.allow_lex_fund_transfer]
}

resource "aws_lex_intent" "withdraw" {
  name        = "Withdraw"
  description = "Intent to withdraw funds"
  sample_utterances = [
    "Withdraw money",
    "I want to take out money",
  ]

  slot {
    name             = "AccountNumber"
    description      = "Account Number from which money will be withdrawn"
    slot_constraint  = "Required"
    slot_type        = "AMAZON.NUMBER"
    priority = 1
    value_elicitation_prompt {
      max_attempts = 2
      message {
        content_type = "PlainText"
        content      = "What is the account number from which you want to withdraw?"
      }
    }
  }

  slot {
    name             = "Amount"
    description      = "Amount to withdraw"
    slot_constraint  = "Required"
    slot_type        = "AMAZON.NUMBER"
    priority = 3
    value_elicitation_prompt {
      max_attempts = 2
      message {
        content_type = "PlainText"
        content      = "How much money would you like to withdraw?"
      }
    }
  }

  slot {
    name             = "Password"
    description      = "Password for authentication"
    slot_constraint  = "Required"
    slot_type        = "AMAZON.AlphaNumeric"
    priority = 2
    value_elicitation_prompt {
      max_attempts = 2
      message {
        content_type = "PlainText"
        content      = "Please provide your password for verification."
      }
    }
  }

  fulfillment_activity {
    type = "CodeHook"
    code_hook {
      message_version = "1.0"
      uri             = var.lambda_function_arns["withdraw"]
    }
  }
  #depends_on = [aws_lambda_permission.allow_lex_withdraw]
}

resource "aws_lex_intent" "balance_enquiry" {
  name        = "BalanceEnquiry"
  description = "Intent to check account balance"
  sample_utterances = [
    "Check my balance",
    "What is my account balance",
  ]

  slot {
    name             = "AccountNumber"
    description      = "Account number to check balance"
    slot_constraint  = "Required"
    slot_type        = "AMAZON.NUMBER"
    priority = 1
    value_elicitation_prompt {
      max_attempts = 2
      message {
        content_type = "PlainText"
        content      = "What is your account number?"
      }
    }
  }

  slot {
    name             = "Password"
    description      = "Password for authentication"
    slot_constraint  = "Required"
    slot_type        = "AMAZON.AlphaNumeric"
    priority = 2
    value_elicitation_prompt {
      max_attempts = 2
      message {
        content_type = "PlainText"
        content      = "Please provide your password for verification."
      }
    }
  }

  fulfillment_activity {
    type = "CodeHook"
    code_hook {
      message_version = "1.0"
      uri             = var.lambda_function_arns["balance_enquiry"]
    }
  }
  #depends_on = [aws_lambda_permission.allow_lex_balance_enquiry]
}

resource "aws_lex_intent" "last_transaction" {
  name        = "LastTransaction"
  description = "Intent to show the last transaction"
  sample_utterances = [
    "Show my last transaction",
    "What was my last transaction",
  ]

  slot {
    name             = "AccountNumber"
    description      = "The account number to fetch the last transaction for"
    slot_constraint  = "Required"
    slot_type        = "AMAZON.NUMBER"
    priority = 1
    value_elicitation_prompt {
      max_attempts = 2
      message {
        content_type = "PlainText"
        content      = "What is your account number?"
      }
    }
  }

  slot {
    name             = "Password"
    description      = "Password for authentication"
    slot_constraint  = "Required"
    slot_type        = "AMAZON.AlphaNumeric"
    priority = 2
    value_elicitation_prompt {
      max_attempts = 2
      message {
        content_type = "PlainText"
        content      = "Please provide your password for verification."
      }
    }
  }

  fulfillment_activity {
    type = "CodeHook"
    code_hook {
      message_version = "1.0"
      uri             = var.lambda_function_arns["last_transaction"]
    }
  }
  #depends_on = [aws_lambda_permission.allow_lex_last_transaction]
}

resource "aws_lex_bot" "BankBot" {
  name        = "BankBot"
  description = "Banking chatbot"
  locale      = "en-US"
  child_directed = false

  clarification_prompt {
    max_attempts = 2
    message {
      content_type = "PlainText"
      content      = "I'm sorry, I didn't understand that. Can you please repeat?"
    }
  }

  abort_statement {
    message {
      content_type = "PlainText"
      content      = "Sorry, I'm not able to help with that."
    }
  }

  intent {
    intent_name = aws_lex_intent.create_account.name
    intent_version = aws_lex_intent.create_account.version
  }

  intent {
    intent_name = aws_lex_intent.delete_account.name
    intent_version = aws_lex_intent.delete_account.version
  }

  intent {
    intent_name = aws_lex_intent.fund_transfer.name
    intent_version = aws_lex_intent.fund_transfer.version
  }

  intent {
    intent_name = aws_lex_intent.withdraw.name
    intent_version = aws_lex_intent.withdraw.version
  }

  intent {
    intent_name = aws_lex_intent.balance_enquiry.name
    intent_version = aws_lex_intent.balance_enquiry.version
  }

  intent {
    intent_name = aws_lex_intent.last_transaction.name
    intent_version = aws_lex_intent.last_transaction.version
  }

  idle_session_ttl_in_seconds = 300
}

resource "aws_lex_bot_alias" "BankBotAlias" {
  bot_name = aws_lex_bot.BankBot.name
  name     = "BankBotAlias"
  description = "Alias for the BankBot"
  bot_version = "$LATEST"
}