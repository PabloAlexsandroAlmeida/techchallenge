resource "aws_glue_job" "glue_etl" {
  name        = var.glue_job_name
  role_arn    = var.role_arn
  command {
    name            = "glueetl"
    script_location = var.script_location
    python_version  = "3"
  }
  glue_version    = "3.0"
  max_capacity    = var.max_capacity
  timeout         = var.timeout
  default_arguments = merge({
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-metrics"                   = "true"
  }, var.additional_arguments)
}
