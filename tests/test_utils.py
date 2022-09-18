import pytest
import logging

from common.utils.logger import getLogger
from common.utils.error_handler import s3_no_such_key_error_handler

from botocore.exceptions import ClientError


def test_logger_initialize(mocker):
    mock_logger = mocker.patch("logging.getLogger")

    getLogger("test name")

    mock_logger.assert_called_with("test name")
    mock_logger().setLevel.assert_called_with(logging.INFO)


def test_s3_no_such_key_error_handler(mocker):
    mock_logger = mocker.patch("logging.Logger.warning")

    error = ClientError({"Error": {"Code": "NoSuchKey"}}, "test")
    logger = getLogger("s3 no such key")

    s3_no_such_key_error_handler(error, logger)
    mock_logger.assert_called_with("No object found")


def test_s3_no_such_key_error_handler_with_exception(mocker):
    error = ClientError({"Error": {"Code": "AnythingElse"}}, "test")
    logger = getLogger("s3 no such key")

    with pytest.raises(ClientError):
        s3_no_such_key_error_handler(error, logger)
