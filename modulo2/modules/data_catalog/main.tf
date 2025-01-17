resource "aws_glue_catalog_database" "catalog_database" {
  name = var.database_name
}

resource "aws_glue_catalog_table" "catalog_table" {
  database_name = aws_glue_catalog_database.catalog_database.name
  name          = var.table_name

  storage_descriptor {
    location      = var.s3_location
    input_format  = var.input_format
    output_format = var.output_format    

    ser_de_info {
      name = var.serde_name
    }
  }
}
