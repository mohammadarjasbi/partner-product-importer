import json
import os
import pytest

from tests import TEST_PATH

from tests.utils import read_file_content_as_string
from lambdas.partner_product_importer import lambda_handler


def test_lambda_handler_handling_invalid_request(mocker):
    mock_logger = mocker.patch("logging.Logger.warning")
    fake_event = {"Records": [{"test": "test"}]}

    lambda_handler(fake_event, None)

    mock_logger.assert_called_with(f"Invalid Request {json.dumps(fake_event)}")


@pytest.mark.parametrize(
    "input_file,output_file",
    [
        ("mock_partner_product_data.xml", "transformed_partner_product_data.json"),
        (
            "mock_partner_partially_valid_product_data.xml",
            "transformed_partner_partially_valid_product_data.json",
        ),
    ],
)
def test_lambda_handler_handling_valid_request(mocker, input_file, output_file):
    mock_s3_manager = mocker.patch("lambdas.partner_product_importer.S3Manager")
    mock_partner_product_data = read_file_content_as_string(
        os.path.join(TEST_PATH, "mock_data", input_file)
    )
    mock_s3_manager().get_file_content.return_value = mock_partner_product_data

    fake_event = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": "fake-bucket"},
                    "object": {"key": "import/fake-key.xml"},
                }
            }
        ]
    }

    lambda_handler(fake_event, None)

    transformed_partner_product_data = read_file_content_as_string(
        os.path.join(TEST_PATH, "mock_data", output_file)
    )

    mock_s3_manager().create_file.assert_called_with(
        transformed_partner_product_data, "partner-data", "export/fake-key.json"
    )
    mock_s3_manager().delete_file.assert_called_with(
        "fake-bucket", "import/fake-key.xml"
    )
