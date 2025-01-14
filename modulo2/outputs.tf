output "lambda_function_name" {
  value = module.lambda_ingestacao.lambda_function_name
}

output "s3_bucket_name" {
  value = module.s3_raw.bucket_name
}
