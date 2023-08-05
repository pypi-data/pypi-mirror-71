import logging
import posixpath
import tempfile

import boto3

logger = logging.getLogger(__name__)

def publish_packages(package_bucket, artifact_config):
    s3_client = boto3.client("s3")

    for source_artifact_name, source_artifact_location in artifact_config["files"].items():
        source_artifact_bucket = source_artifact_location["bucket"]
        source_artifact_key = source_artifact_location["key"]

        with tempfile.TemporaryFile() as source_artifact_file:
            s3_client.download_fileobj(
                source_artifact_bucket,
                source_artifact_key,
                source_artifact_file
            )

            source_artifact_file.seek(0)

            source_artifact_filename = posixpath.basename(source_artifact_key)
            _, source_artifact_extension = posixpath.splitext(source_artifact_filename)

            package_artifact_filename = "latest" + source_artifact_extension
            package_key = posixpath.join(source_artifact_name, package_artifact_filename)

            logger.info(
                "Publishing package artifact from s3://%s/%s to s3://%s/%s",
                source_artifact_bucket,
                source_artifact_key,
                package_bucket,
                package_key
            )

            s3_client.upload_fileobj(source_artifact_file, package_bucket, package_key)