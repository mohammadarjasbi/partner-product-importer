import os
import pytest

from common.utils.s3_manager import S3Manager
from common.env import env


def test_s3_manager_initialize(mocker):
    mock_boto3 = mocker.patch("boto3.resource")

    S3Manager()

    mock_boto3.assert_called_with("s3", endpoint_url=env.get("LOCALSTACK_ENDPOINT_URL"))


def test_s3_manager_get_file_content(mocker):
    mock_boto3 = mocker.patch("boto3.resource")
    mock_logger = mocker.patch("logging.Logger.info")

    s3_manger = S3Manager()
    s3_manger.get_file_content("fake-bucket", "fake-key.xml")

    mock_logger.assert_called_with(
        f'Get content of {os.path.join("fake-bucket","fake-key.xml")}'
    )
    mock_boto3().Object.assert_called_with("fake-bucket", "fake-key.xml")
    assert mock_boto3().Object().get.call_count == 1


def test_s3_manager_create_file(mocker):
    mock_boto3 = mocker.patch("boto3.resource")
    mock_logger = mocker.patch("logging.Logger.info")

    s3_manger = S3Manager()
    s3_manger.create_file("test data", "fake-bucket", "fake-key.json")

    mock_logger.assert_called_with(
        f'Create {os.path.join("fake-bucket","fake-key.json")}'
    )
    mock_boto3().Object.assert_called_with("fake-bucket", "fake-key.json")
    mock_boto3().Object().put.assert_called_with(Body="test data")


def test_s3_manager_delete_file(mocker):
    mock_boto3 = mocker.patch("boto3.resource")
    mock_logger = mocker.patch("logging.Logger.info")

    s3_manger = S3Manager()
    s3_manger.delete_file("fake-bucket", "fake-key.xml")

    mock_logger.assert_called_with(
        f'Delete {os.path.join("fake-bucket","fake-key.xml")}'
    )
    mock_boto3().Object.assert_called_with("fake-bucket", "fake-key.xml")
    assert mock_boto3().Object().delete.call_count == 1
