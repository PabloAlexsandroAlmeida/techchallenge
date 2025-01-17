variable "glue_job_name" {}
variable "role_arn" {}
variable "script_location" {}
variable "max_capacity" {
  default = 2
}
variable "timeout" {
  default = 10
}
variable "additional_arguments" {
  default = {}
}
