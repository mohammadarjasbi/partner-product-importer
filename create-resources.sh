#!/bin/bash

LOCALSTACK_ENDPOINT_URL="http://localhost:4566"

echo "Create lambda function"
aws \
    --endpoint-url=$LOCALSTACK_ENDPOINT_URL \
    lambda create-function --function-name partner-product-importer \
    --zip-file fileb://lambdas/function.zip \
    --handler partner_product_importer.lambda_handler \
    --timeout 900 --runtime python3.8 \
    --role arn:aws:iam::000000000000:role/lambda-role

echo "Make partner S3 bucket"
aws \
    s3 mb s3://partner-data \
    --endpoint-url $LOCALSTACK_ENDPOINT_URL

echo "Create notification configuration"
aws \
    --endpoint-url=$LOCALSTACK_ENDPOINT_URL \
    s3api put-bucket-notification-configuration --bucket partner-data \
    --notification-configuration file://config/s3-notif-config.json

echo "All resources initialized! 🚀"
