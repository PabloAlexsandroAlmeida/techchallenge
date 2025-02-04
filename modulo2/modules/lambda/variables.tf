variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "lambda_role_arn" {
  description = "ARN of the IAM role for Lambda"
  type        = string
}

variable "lambda_package_path" {
  description = "Path to the Lambda package"
  type        = string
}

variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "iam_policy_attachment" {
  description = "IAM policy attachment dependency"
  type        = any
}

variable "s3_bucket" {
  description = "Name of the S3 bucket for lambda deploy"
  type        = string
}

variable "s3_key" {
  description = "Name of the S3 bucke deploy key"
  type        = string
}

