import argparse
import json
import logging

from vat_package_utils import publish

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-bucket", required=True)
    parser.add_argument("--artifact-config", required=True)
    args = parser.parse_args()

    with open(args.artifact_config) as artifact_config_file:
        artifact_config = json.load(artifact_config_file)

    publish.publish_packages(args.package_bucket, artifact_config)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    main()
