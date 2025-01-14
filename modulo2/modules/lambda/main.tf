resource "aws_lambda_function" "b3_lambda" {
  function_name = var.lambda_function_name
  role          = var.lambda_role_arn
  handler       = "lambda_handler.lambda_handler"
  runtime       = "python3.11"
  timeout       = 5

  s3_bucket = var.s3_bucket
  s3_key    = var.s3_key

  # Opcional: atualize a função quando o pacote mudar
  source_code_hash = filebase64sha256(var.lambda_package_path)

  environment {
    variables = {
      BUCKET_NAME = var.bucket_name
    }
  }
  
  layers = [
    "arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python311:20"
  ]

  depends_on = [var.iam_policy_attachment]
}
