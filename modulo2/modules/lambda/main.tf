# Log Group para a Lambda
resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${var.lambda_function_name}"
  retention_in_days = 7
}

# Função Lambda
resource "aws_lambda_function" "b3_lambda" {
  function_name = var.lambda_function_name
  role          = aws_iam_role.lambda_execution_role.arn
  handler       = "lambda_handler.lambda_handler"
  runtime       = "python3.11"
  timeout       = 5

  s3_bucket = var.s3_bucket
  s3_key    = var.s3_key

  source_code_hash = filebase64sha256(var.lambda_package_path)
  
  layers = [
    "arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python311:20"
  ]
}

# Política IAM para Logs no CloudWatch
resource "aws_iam_policy" "lambda_logging_policy" {
  name        = "${var.lambda_function_name}-logging-policy"
  description = "Permite que a Lambda grave logs no CloudWatch"
  
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action   = [
          "logs:CreateLogGroup", 
          "logs:CreateLogStream", 
          "logs:PutLogEvents",
          "s3:PutObject",
          "s3:ListBucket",
          "s3:GetObject",
          "lambda:GetLayerVersion",
          "glue:StartJobRun"],
        Effect   = "Allow",
        Resource = "*"
      }
    ]
  })
}

# Role da Lambda
resource "aws_iam_role" "lambda_execution_role" {
  name               = "${var.lambda_function_name}-execution-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Anexar a política de logging ao role
resource "aws_iam_role_policy_attachment" "lambda_logging_policy_attachment" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_logging_policy.arn
}
