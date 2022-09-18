import os
import boto3

from .logger import getLogger
from common.env import env

logger = getLogger("S3")


class S3Manager:
    def __init__(self):
        self.s3 = boto3.resource("s3", endpoint_url=env.get("LOCALSTACK_ENDPOINT_URL"))

    def get_file_content(self, bucket_name: str, file_key: str):
        logger.info(f"Get content of {os.path.join(bucket_name, file_key)}")
        s3_object = self.s3.Object(bucket_name, file_key)
        file_content = s3_object.get()["Body"].read().decode("utf-8")
        return file_content

    def create_file(self, body: str, bucket_name: str, file_key: str):
        logger.info(f"Create {os.path.join(bucket_name, file_key)}")
        s3_object = self.s3.Object(bucket_name, file_key)
        s3_object.put(Body=body)

    def delete_file(self, bucket_name: str, file_key: str):
        logger.info(f"Delete {os.path.join(bucket_name, file_key)}")
        self.s3.Object(bucket_name, file_key).delete()
