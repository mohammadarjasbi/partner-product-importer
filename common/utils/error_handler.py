def s3_no_such_key_error_handler(error, logger):
    if error.response["Error"]["Code"] == "NoSuchKey":
        logger.warning("No object found")
        return
    else:
        raise error
