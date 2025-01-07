module "s3" {
  source      = "./modules/s3"
  bucket_name = var.s3_bucket_name
}

module "iam" {
  source      = "./modules/iam"
  role_name   = var.lambda_role_name
  bucket_name = module.s3.bucket_name
}

module "lambda" {
  source                = "./modules/lambda"
  lambda_function_name  = var.lambda_function_name
  lambda_role_arn       = module.iam.role_arn
  lambda_package_path   = "lambda_package.zip"
  bucket_name           = module.s3.bucket_name
  iam_policy_attachment = module.iam.role_arn
}
