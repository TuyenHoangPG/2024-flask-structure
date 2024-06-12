import os
from uuid import uuid4

import boto3
from flask import current_app
from werkzeug.utils import secure_filename

from ...commons.configs.config import get_config
from ...commons.constants.message import ERROR_MESSSAGE
from ...commons.extensions import Singleton
from ...commons.middlewares.exception import ApiException


class S3StorageService(Singleton):
    config = get_config(os.getenv("FLASK_ENV"))

    s3 = boto3.client(
        "s3",
        aws_access_key_id=config.S3_ACCESS_KEY,
        aws_secret_access_key=config.S3_SECRET_KEY,
        region_name=config.S3_REGION,
    )

    def upload_file_to_s3(self, file, path, file_name=None, content_type=None):
        filename = file_name if file_name else secure_filename(file.filename)
        key = f"{path}/{uuid4()}-{filename}"

        try:
            self.s3.upload_fileobj(
                file,
                Bucket=self.config.S3_BUCKET_NAME,
                Key=key,
                ExtraArgs={
                    "ContentType": content_type if content_type else file.content_type
                },
            )

        except Exception as e:
            print(f"Error when upload file to S3. error = {e}")
            current_app.logger.error(f"Error when upload file to S3. error = {e}")
            raise ApiException(ERROR_MESSSAGE.SERVER_ERROR, status_code=500)

        return {
            "key": key,
            "filename": filename,
            "file": file,
        }

    def generate_signed_url(self, key):
        expiration_seconds = 60 * 60  # 1 hour
        signed_url = self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.config.S3_BUCKET_NAME, "Key": key},
            ExpiresIn=expiration_seconds,
        )

        return signed_url

    def get_object(self, key):
        response = self.s3.get_object(Bucket=self.config.S3_BUCKET_NAME, Key=key)
        return response
