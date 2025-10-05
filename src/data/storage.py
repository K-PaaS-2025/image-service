import boto3
from botocore.exceptions import ClientError

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class NCloudStorage:
    def __init__(self):
        self.endpoint_url = 'https://kr.object.ncloudstorage.com'
        self.region_name = 'kr-standard'
        self.access_key = os.getenv('NCLOUD_ACCESS_KEY')
        self.secret_key = os.getenv('NCLOUD_SECRET_KEY')
        self.bucket_name = os.getenv('NCLOUD_BUCKET_NAME')

        if not all([self.access_key, self.secret_key, self.bucket_name]):
            raise ValueError("Missing required NCloud storage credentials")

        self.s3_client = boto3.client(
            's3',
            endpoint_url=self.endpoint_url,
            region_name=self.region_name,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
        )

    def upload_fileobj(self, file_obj, object_key: str) -> Optional[str]:
        try:
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                object_key,
                ExtraArgs={'ACL': 'public-read'}
            )
            logger.info(f"Successfully uploaded file object to {object_key}")

            url = f"{self.endpoint_url}/{self.bucket_name}/{object_key}"
            return url

        except ClientError as e:
            logger.error(f"Failed to upload file object: {e}")
            return None
