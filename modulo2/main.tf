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

  lambda_function_name  = "lambda-ingestao"
  lambda_role_arn       = module.iam.role_arn
  lambda_package_path   = "lambda-ingestao.zip"
  bucket_name           = module.s3_raw.bucket_name
  iam_policy_attachment = module.iam.role_arn
  s3_bucket             = aws_s3_bucket.lambda_deployments_ingestao.bucket
  s3_key                = aws_s3_object.lambda_package_ingestao.key

  depends_on = [
    module.s3_raw,
    module.iam
  ]
}


// Bucket para carregar a lambda de glue ela possui mais de 50MB
resource "aws_s3_bucket" "lambda_deployments_glue" {
  bucket = "897722708429-lambda-deployments-glue"
}

// Recuso para fazer upload do lambda glue no s3
resource "aws_s3_object" "lambda_package_glue" {
  bucket = aws_s3_bucket.lambda_deployments_glue.bucket
  key    = "lambda-glue.zip"
  source = "lambda-glue.zip"
}

// Adiciona a configuração de notificação de eventos para o bucket S3
resource "aws_s3_bucket_notification" "raw_bucket_notification" {
  bucket = module.s3_raw.bucket_name

  lambda_function {
    lambda_function_arn = module.lambda_glue.lambda_function_arn
    events              = ["s3:ObjectCreated:*"] // Dispara a Lambda para qualquer objeto criado
    filter_prefix       = "" // Opcional: Filtra objetos com prefixo específico
    filter_suffix       = "" // Opcional: Filtra objetos com sufixo específico
  }

  depends_on = [aws_lambda_permission.s3_invoke_lambda_glue]
}

// Lambda de glue
module "lambda_glue" {
  source                = "./modules/lambda"

  lambda_function_name  = "lambda-glue"
  lambda_role_arn       = module.iam.role_arn
  lambda_package_path   = "lambda-glue.zip"
  bucket_name           = module.s3_refined.bucket_name
  iam_policy_attachment = module.iam.role_arn
  s3_bucket             = aws_s3_bucket.lambda_deployments_glue.bucket
  s3_key                = aws_s3_object.lambda_package_glue.key

  depends_on = [
    module.s3_refined,
    module.iam
  ]
}

// Permissão para o S3 invocar a Lambda
resource "aws_lambda_permission" "s3_invoke_lambda_glue" {
  statement_id  = "AllowS3InvokeGlueLambda"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_glue.lambda_function_name
  principal     = "s3.amazonaws.com"
  source_arn    = module.s3_raw.bucket_arn

  depends_on = [
    module.lambda_glue,
    module.s3_raw
  ]
}


// Data catalog
module "data_catalog" {
  source        = "./modules/data_catalog"
  database_name = "pos-tech"
  table_name    = "challenge"
  s3_location   = module.s3_raw.bucket_name
  input_format  = "org.apache.hadoop.mapred.TextInputFormat"
  output_format = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"
  serde_name    = "org.apache.hadoop.hive.serde2.OpenCSVSerde"
}

// GLue ETL
resource "aws_iam_role" "glue_execution_role" {
  name = "glue-execution-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "glue_execution_policy" {
  name = "glue_execution_policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["*"]
        Resource = ["*"]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_policy_glue" {
  role       = aws_iam_role.glue_execution_role.name
  policy_arn = aws_iam_policy.glue_execution_policy.arn
}


// Bucket temp
resource "aws_s3_bucket" "glue-temp" {
  bucket = "897722708429-glue-temp"
}

resource "aws_s3_bucket" "glue-etl-script" {
  bucket = "897722708429-glue-etl-script"
}

// S3 bucket para script glue etl
resource "aws_s3_object" "glue-tl-script" {
  bucket = aws_s3_bucket.glue-etl-script.bucket
  key    = "glue-etl-script.py"
  source = "glue-etl-script.py"
}

module "glue_etl" {
  source              = "./modules/glue"
  glue_job_name       = "pos-tech"
  role_arn            = aws_iam_role.glue_execution_role.arn
  script_location     = "s3://897722708429-glue-etl-script/glue-etl-script.py"
  max_capacity        = 5
  timeout             = 5
  additional_arguments = {
    "--TempDir" = "s3://897722708429-glue-temp/"
  }
  depends_on = [
    aws_iam_role.glue_execution_role
  ]
}

