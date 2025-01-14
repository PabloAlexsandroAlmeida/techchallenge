#!/bin/bash

mv lambda-ingestao/lambda_handler.py .
mv lambda-ingestao/requirements.txt .

cd lambda-ingestao
rm -rf * -y 
ls -lart

cd ..

mv lambda_handler.py lambda-ingestao
mv requirements.txt lambda-ingestao

./sript/packing.sh lambda-ingestao/ lambda-ingestao.zip