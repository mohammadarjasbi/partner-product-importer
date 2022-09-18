import os

env = {
    "LOCALSTACK_ENDPOINT_URL": os.getenv(
        "LOCALSTACK_ENDPOINT_URL",
        f'http://{os.getenv("LOCALSTACK_HOSTNAME", "localhost")}:4566',
    ),
    "EXPORT_PARTNER_PRODUCTS_BUCKET": os.getenv(
        "EXPORT_PARTNER_PRODUCTS_BUCKET", "partner-data"
    ),
    "EXPORT_PARTNER_PRODUCTS_FILE_KEY": os.getenv(
        "EXPORT_PARTNER_PRODUCTS_FILE_KEY", "export/"
    ),
}
