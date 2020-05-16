#!/bin/sh

mkdir -p tmp
cp *.py tmp/
pip3 install -r requirements.txt -t tmp/
cd tmp
zip amazonForYNAB.zip -r *

# aws lambda create-function --function-name amazonForYNAB --zip-file fileb://amazonForYNAB.zip --handler main.py --runtime python3.8 --role  arn:aws:iam::961506973552:role/lambda-ex
aws lambda update-function-code --function-name amazonForYNAB --zip-file fileb://amazonForYNAB.zip 
aws lambda update-function-configuration --function-name amazonForYNAB --timeout 45