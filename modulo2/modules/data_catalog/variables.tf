variable "database_name" {}
variable "table_name" {}
variable "s3_location" {}
variable "input_format" {
  default = "org.apache.hadoop.mapred.TextInputFormat"
}
variable "output_format" {
  default = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"
}
variable "serde_name" {
  default = "org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe"
}
