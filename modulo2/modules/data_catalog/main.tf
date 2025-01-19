resource "aws_glue_catalog_database" "catalog_database" {
  name = var.database_name
}

resource "aws_glue_catalog_table" "catalog_table" {
  database_name = aws_glue_catalog_database.catalog_database.name
  name          = var.table_name

  storage_descriptor {
    location      = "s3://897722708429-refined/"
    input_format  = var.input_format
    output_format = var.output_format    

    ser_de_info {
      name = var.serde_name
    }
  }

  table_type = "EXTERNAL_TABLE" # Necessário para que Athena reconheça como tabela externa
    parameters = {
      classification = "parquet" # Ajuste para o formato do arquivo (ex: parquet, csv, etc.)
      "skip.header.line.count" = "1" # Opcional: Ignora cabeçalhos
    }

}
