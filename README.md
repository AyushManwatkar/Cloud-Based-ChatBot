<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Banking_ChatBot README</title>
</head>
<body>
    <h1>Banking_ChatBot</h1>
    <h2>Overview</h2>
    <p>
        Banking_ChatBot is an intelligent chatbot designed to assist with common banking tasks such as creating accounts, transferring funds, withdrawing money, checking account balances, deleting accounts, and viewing the last transaction. This project utilizes Amazon Lex for natural language understanding, AWS Lambda for executing business logic, and DynamoDB for data storage.
    </p>
    <img src="Architecture.jpg" alt="Architectural Diagram of Banking_ChatBot" style="max-width:100%; height:auto;">
    <h2>Features</h2>
    <ul>
        <li><strong>Create Account</strong>: Allows users to create new banking accounts seamlessly.</li>
        <li><strong>Fund Transfer</strong>: Facilitates the transfer of funds between accounts.</li>
        <li><strong>Withdraw</strong>: Enables users to withdraw money from their accounts.</li>
        <li><strong>Check Balance</strong>: Provides users with the ability to check their account balances.</li>
        <li><strong>Delete Account</strong>: Allows users to delete their banking accounts.</li>
        <li><strong>Last Transaction</strong>: Shows the last transaction details for a given account.</li>
    </ul>
    <h2>Technologies Used</h2>
    <ul>
        <li><strong>Amazon Lex</strong>: For building the conversational interface of the chatbot.</li>
        <li><strong>AWS Lambda</strong>: To handle backend logic and integrations.</li>
        <li><strong>DynamoDB</strong>: To store user data and transaction records.</li>
    </ul>
    <h2>Getting Started</h2>
    <p>
        To set up and deploy the Banking_ChatBot, follow these steps:
    </p>
    <h3>Prerequisites</h3>
    <ul>
        <li>An AWS account</li>
        <li>AWS CLI installed and configured</li>
        <li>Python 3.x installed</li>
    </ul>
    <h3>Setup</h3>
    <ol>
        <li>Create an IAM role:
            <ul>
                <li>Go to the IAM console in AWS.</li>
                <li>Create a new role with the service <strong>Lambda</strong>.</li>
                <li>Attach policies for full access to <strong>DynamoDB</strong>, <strong>Lambda</strong>, and <strong>CloudFront</strong>.</li>
            </ul>
        </li>
        <li>Clone the repository:
            <pre><code>git clone https://github.com/yourusername/Banking_ChatBot.git</code></pre>
        </li>
        <li>Navigate to the project directory:
            <pre><code>cd Banking_ChatBot</code></pre>
        </li>
        <li>Deploy AWS Lambda functions:
            <ul>
                <li>Upload the Lambda function ZIP files:
                    <pre><code>aws lambda create-function --function-name create_account --zip-file fileb://zip_files/create_account.zip --handler create_account.lambda_handler --runtime python3.8 --role arn:aws:iam::your-account-id:role/your-lambda-role</code></pre>
                    <pre><code>aws lambda create-function --function-name fund_transfer --zip-file fileb://zip_files/fund_transfer.zip --handler fund_transfer.lambda_handler --runtime python3.8 --role arn:aws:iam::your-account-id:role/your-lambda-role</code></pre>
                    <pre><code>aws lambda create-function --function-name withdraw --zip-file fileb://zip_files/withdraw.zip --handler withdraw.lambda_handler --runtime python3.8 --role arn:aws:iam::your-account-id:role/your-lambda-role</code></pre>
                    <pre><code>aws lambda create-function --function-name balance_enquiry --zip-file fileb://zip_files/balance_enquiry.zip --handler balance_enquiry.lambda_handler --runtime python3.8 --role arn:aws:iam::your-account-id:role/your-lambda-role</code></pre>
                    <pre><code>aws lambda create-function --function-name delete_account --zip-file fileb://zip_files/delete_account.zip --handler delete_account.lambda_handler --runtime python3.8 --role arn:aws:iam::your-account-id:role/your-lambda-role</code></pre>
                    <pre><code>aws lambda create-function --function-name last_transaction --zip-file fileb://zip_files/last_transaction.zip --handler last_transaction.lambda_handler --runtime python3.8 --role arn:aws:iam::your-account-id:role/your-lambda-role</code></pre>
                </li>
            </ul>
        </li>
        <li>Set up DynamoDB tables:
            <ul>
                <li>Create a table named <strong>customerdetails</strong> with <strong>accountnumber</strong> as the primary key (String type).</li>
                <li>Update the table name in all Lambda functions if necessary.</li>
            </ul>
        </li>
        <li>Create and configure Amazon Lex bot:
            <ul>
                <li>Navigate to the Amazon Lex console.</li>
                <li>Create a new bot and import the intents from the provided <code>Banking_ChatBot_Export.json</code> file.</li>
                <li>Link the bot with the corresponding Lambda functions.</li>
            </ul>
        </li>
        <li>Deploy the Terraform configuration:
            <ul>
                <li>Ensure you have Terraform installed. Follow the installation instructions in the <a href="#terraform-installation">Terraform Installation</a> section.</li>
                <li>Initialize Terraform:
                    <pre><code>terraform init</code></pre>
                </li>
                <li>Apply the Terraform configuration:
                    <pre><code>terraform apply</code></pre>
                </li>
            </ul>
        </li>
    </ol>
    <h2>Usage</h2>
    <p>
        Once the bot is set up, you can interact with it via the Amazon Lex console or integrate it into your applications to start managing banking tasks through conversations.
    </p>
    <h2>Repository Structure</h2>
    <ul>
        <li><code>modules/dynamodb/main.tf</code>: Terraform configuration for DynamoDB setup.</li>
        <li><code>modules/iam/main.tf</code>: Terraform configuration for IAM role setup.</li>
        <li><code>modules/lambda/main.tf</code>: Terraform configuration for Lambda function setup.</li>
        <li><code>modules/lex/main.tf</code>: Terraform configuration for Lex bot setup.</li>
        <li><code>zip_files/create_account.zip</code>: ZIP file for the create account Lambda function.</li>
        <li><code>zip_files/fund_transfer.zip</code>: ZIP file for the fund transfer Lambda function.</li>
        <li><code>zip_files/withdraw.zip</code>: ZIP file for the withdraw Lambda function.</li>
        <li><code>zip_files/balance_enquiry.zip</code>: ZIP file for the balance enquiry Lambda function.</li>
        <li><code>zip_files/delete_account.zip</code>: ZIP file for the delete account Lambda function.</li>
        <li><code>zip_files/last_transaction.zip</code>: ZIP file for the last transaction Lambda function.</li>
        <li><code>main.tf</code>: Root Terraform configuration file that includes all modules.</li>
    </ul>
    <h2>Note</h2>
    <p>
        For simplicity, each banking task is handled by a separate Lambda function. However, it is possible to combine these into a single function if preferred.
    </p>
    <h2 id="terraform-installation">Terraform Installation</h2>
    <h3>Installing Terraform</h3>
    <ol>
        <li>Download the appropriate Terraform binary for your operating system from the <a href="https://www.terraform.io/downloads.html">Terraform website</a>.</li>
        <li>Extract the binary from the downloaded archive.</li>
        <li>Move the extracted binary to a directory included in your system's PATH (e.g., <code>/usr/local/bin</code> on macOS/Linux or <code>C:\Program Files\Terraform</code> on Windows).</li>
        <li>Verify the installation by running:
            <pre><code>terraform --version</code></pre>
        </li>
    </ol>
    <h3>Configuring AWS CLI</h3>
    <ol>
        <li>Install AWS CLI by following the instructions on the <a href="https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html">AWS CLI installation guide</a>.</li>
        <li>Configure AWS CLI with your credentials:
            <pre><code>aws configure</code></pre>
            <ul>
                <li>Enter your AWS Access Key ID.</li>
                <li>Enter your AWS Secret Access Key.</li>
                <li>Select the default region name (e.g., <code>us-east-1</code>).</li>
                <li>Select the default output format (e.g., <code>json</code>).</li>
            </ul>
        </li>
    </ol>
</body>
</html>
