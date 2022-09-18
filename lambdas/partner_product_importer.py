import os
import json

from common.env import env
from common.utils.logger import getLogger
from common.utils.s3_manager import S3Manager
from common.utils.error_handler import s3_no_such_key_error_handler
from common.transformer.xml_partner_product_transformer import (
    XMLPartnerProductTransformer,
)

from botocore.exceptions import ClientError


logger = getLogger("Partner Product Importer")


def lambda_handler(event, context):
    logger.info("Start partner product importing process")

    for record in event.get("Records"):
        s3_record_data = record.get("s3", {})
        bucket_name = s3_record_data.get("bucket", {}).get("name")
        file_key = s3_record_data.get("object", {}).get("key")

        if not bucket_name or not file_key:
            logger.warning(f"Invalid Request {json.dumps(event)}")
            return True

        s3 = S3Manager()

        try:
            xml_file_content = s3.get_file_content(bucket_name, file_key)
        except ClientError as e:
            return s3_no_such_key_error_handler(e, logger)

        xml_partner_product_transformer = XMLPartnerProductTransformer(xml_file_content)
        xml_partner_product_transformer.transform()
        transformed_product_data_in_json = xml_partner_product_transformer.get_json()

        file_name_without_extension = os.path.basename(file_key).split(".")[0]
        file_name = f"{file_name_without_extension}.json"

        s3.create_file(
            json.dumps(transformed_product_data_in_json),
            env.get("EXPORT_PARTNER_PRODUCTS_BUCKET"),
            os.path.join(
                env.get("EXPORT_PARTNER_PRODUCTS_FILE_KEY"),
                file_name,
            ),
        )

        try:
            s3.delete_file(bucket_name, file_key)
        except ClientError as e:
            return s3_no_such_key_error_handler(e, logger)
