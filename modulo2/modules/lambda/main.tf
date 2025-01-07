resource "aws_lambda_function" "b3_lambda" {
  filename         = var.lambda_package_path
  function_name    = var.lambda_function_name
  role             = var.lambda_role_arn
  handler          = "main.lambda_handler"
  runtime          = "python3.11"
  source_code_hash = filebase64sha256(var.lambda_package_path)

  environment {
    variables = {
      BUCKET_NAME = var.bucket_name
    }
  }

  depends_on = [var.iam_policy_attachment]
}
