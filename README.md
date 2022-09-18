# Partner Product Importer

## Running Instructions
After cloning this repository, enter this command in your terminal to run this project:
```
docker compose up
```
You'll see this log-in terminal a few minutes later:
```
All resources initialized! 🚀
```

Now you can move the test partner product file to the S3 bucket on Loaclstack:
```
aws --endpoint-url=http://localhost:4566 s3 cp tests/mock_data/mock_partner_product_data.xml  s3://partner-data/import/mock_partner_product_data.xml
```

With this command, you can see the lambda function logs after a few seconds (It may even take a couple of minutes since Localstack is a bit slow):
```
aws --endpoint-url=http://localhost:4566 --region us-east-1 logs tail '/aws/lambda/partner-product-importer' --follow
```

After that you can download the transformed file from S3 by this command:
```
aws --endpoint-url=http://localhost:4566 s3 cp s3://partner-data/export/mock_partner_product_data.json mock_partner_product_data.json
```

## Test

You can run unit tests by using these commands:
```
pip install -r lambdas/requirements.txt -r lambdas/requirements-build.txt
```
The command above will install needed dependencies for both test files and used libraries in order to run tests properly.

Run these commands in order to run tests and create a coverage report file:
```
python -m coverage run -m pytest tests 
```

Also, you can see the coverage report by using the command below:
```
python -m coverage report    
```

**This project has 97% test coverage**


# Structure

## Why lambda?

* Lambda has some options that you can schedule your task with it, and you can trigger it when a condition that you've provided for it happens (in this case if any XML file is created or updated in S3 Bucket).

* Besides Lambda has 15 minutes (900 Second) time-out duration that would fit our stressed required situation (around 10k records), so our function had enough time to process our data. 

* I could've used other methods for it Ex. Corn Job, ECS task (Which I'm not too familiar with it), etc. but Lambda is a better match considering costs and resources.

* last but not least, in other structures, our function must have remained Run in order to check if some files are created or not, or optimistically we had to force our function to run accordingly at some specific due ex. every 2 hours.

## File Structure

* I've tried to implement logic and modifications in a way that we could call modularised and reusable.

* Files and Structures are created in a way that could be used for production and development with the minimum problems (It's not perfect, but I think it could be improved)

