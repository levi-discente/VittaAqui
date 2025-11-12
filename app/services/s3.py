"""AWS S3 service for handling image uploads."""

import logging
import uuid
from typing import BinaryIO

import boto3
from botocore.exceptions import ClientError

from app.core.config import settings

logger = logging.getLogger(__name__)


class S3Service:
    """Service for uploading images to AWS S3."""

    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
        )
        self.bucket_name = settings.aws_s3_bucket
        self.region = settings.aws_region

    def upload_profile_image(
        self, file_content: bytes | BinaryIO, file_name: str, user_id: int
    ) -> dict:
        """
        Upload a profile image to S3.

        Args:
            file_content: The image file content (bytes or file-like object)
            file_name: Original filename
            user_id: User ID for organizing uploads

        Returns:
            dict: Upload response containing url and key
        """
        try:
            logger.info(f"Starting S3 upload for user {user_id}")
            logger.info(f"File name: {file_name}, File type: {type(file_content)}")

            # Generate unique filename
            file_extension = file_name.split(".")[-1] if "." in file_name else "jpg"
            unique_filename = f"profile_images/user_{user_id}/{uuid.uuid4()}.{file_extension}"

            logger.info(f"Uploading to S3: {unique_filename}")

            # Determine content type
            content_type = self._get_content_type(file_extension)

            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=unique_filename,
                Body=file_content,
                ContentType=content_type,
            )

            # Generate public URL
            url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{unique_filename}"

            logger.info(f"Upload successful! URL: {url}")
            return {
                "url": url,
                "key": unique_filename,
            }
        except ClientError as e:
            logger.error(f"S3 upload error: {str(e)}", exc_info=True)
            raise ValueError(f"S3 upload failed: {str(e)}")
        except Exception as e:
            logger.error(f"S3 upload exception: {str(e)}", exc_info=True)
            raise

    def delete_image(self, key: str) -> bool:
        """
        Delete an image from S3.

        Args:
            key: The S3 object key

        Returns:
            bool: True if deletion was successful
        """
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
            logger.info(f"Deleted image from S3: {key}")
            return True
        except ClientError as e:
            logger.error(f"S3 delete error: {str(e)}")
            return False

    def _get_content_type(self, extension: str) -> str:
        """Get content type based on file extension."""
        content_types = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "gif": "image/gif",
            "webp": "image/webp",
            "svg": "image/svg+xml",
        }
        return content_types.get(extension.lower(), "image/jpeg")


# Singleton instance
s3_service = S3Service()
