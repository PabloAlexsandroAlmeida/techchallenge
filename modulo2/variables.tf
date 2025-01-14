variable "lambda_function_name" {
  default = "lambda-ingestao"
}

variable "s3_bucket_name_raw" {
  default = "897722708429-raw"
}

variable "s3_bucket_name_refined" {
  default = "897722708429-refined"
}

variable "lambda_role_name" {
  default = "lambda_execution_role"
}
