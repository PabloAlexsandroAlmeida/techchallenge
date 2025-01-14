// Bucket para arquivos temporario
module "s3_raw" {
  source      = "./modules/s3"
  bucket_name = var.s3_bucket_name_raw
}

// Bucket para arquivos refinados pelo GLue
module "s3_refined" {
  source      = "./modules/s3"
  bucket_name = var.s3_bucket_name_refined
}

// IAM com permissao a lamnda de ingestao
module "iam" {
  source      = "./modules/iam"
  role_name   = var.lambda_role_name
  bucket_name = module.s3_raw.bucket_name
}

// Bucket para carregar a lambda de ingestao ela possui mais de 50MB
resource "aws_s3_bucket" "lambda_deployments_ingestao" {
  bucket = "897722708429-lambda-deployments-ingestao"
}

// Recuso para fazer upload do lambda no s3
resource "aws_s3_object" "lambda_package_ingestao" {
  bucket = aws_s3_bucket.lambda_deployments_ingestao.bucket
  key    = "lambda-ingestao.zip"
  source = "lambda-ingestao.zip"
}

// Lambda de ingestao
module "lambda_ingestacao" {
  source                = "./modules/lambda"

  lambda_function_name  = var.lambda_function_name
  lambda_role_arn       = module.iam.role_arn
  lambda_package_path   = "lambda-ingestao.zip"
  bucket_name           = module.s3_raw.bucket_name
  iam_policy_attachment = module.iam.role_arn
  s3_bucket             = aws_s3_bucket.lambda_deployments_ingestao.bucket
  s3_key                = aws_s3_object.lambda_package_ingestao.key
}
