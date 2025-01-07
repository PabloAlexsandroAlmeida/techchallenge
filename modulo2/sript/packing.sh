#!/bin/bash
set -e

LAMBDA_DIR=$1
ZIP_FILE="lambda_package.zip"

# Remover pacote anterior
rm -f $ZIP_FILE

# Instalar dependências
pip install -r $LAMBDA_DIR/requirements.txt -t $LAMBDA_DIR

# Compactar a Lambda
cd $LAMBDA_DIR
zip -r ../$ZIP_FILE .
cd ..

echo "Lambda package created: $ZIP_FILE"
