"""ImageKit service for handling image uploads."""

import base64
from typing import BinaryIO

from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

from app.core.config import settings


class ImageKitService:
    """Service for uploading images to ImageKit."""

    def __init__(self):
        self.imagekit = ImageKit(
            private_key=settings.imagekit_private_key,
            public_key=settings.imagekit_public_key,
            url_endpoint=settings.imagekit_url_endpoint,
        )

    def upload_profile_image(
        self, file_content: bytes | BinaryIO, file_name: str, user_id: int
    ) -> dict:
        """
        Upload a profile image to ImageKit.

        Args:
            file_content: The image file content (bytes or file-like object)
            file_name: Original filename
            user_id: User ID for organizing uploads

        Returns:
            dict: Upload response containing url, fileId, etc.
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            logger.info(f"Starting ImageKit upload for user {user_id}")
            logger.info(f"File name: {file_name}, File type: {type(file_content)}")
            
            # Convert bytes to base64 if needed
            if isinstance(file_content, bytes):
                logger.info(f"Converting {len(file_content)} bytes to base64")
                file_content = base64.b64encode(file_content).decode("utf-8")

            # Create upload options
            options = UploadFileRequestOptions(
                use_unique_file_name=True,
                tags=["profile", f"user_{user_id}"],
                folder=f"/profile_images/user_{user_id}",
                response_fields=["url", "fileId", "name", "size", "filePath"],
            )

            logger.info("Calling ImageKit upload_file...")
            logger.info(f"Options created: use_unique_file_name=True, folder={options.folder}")
            
            result = self.imagekit.upload_file(
                file=file_content,
                file_name=file_name,
                options=options
            )

            if hasattr(result, "error") and result.error:
                logger.error(f"ImageKit returned error: {result.error}")
                raise ValueError(f"ImageKit upload failed: {result.error}")

            logger.info(f"Upload successful! URL: {result.url}")
            return {
                "url": result.url,
                "file_id": result.file_id,
                "name": result.name,
                "file_path": result.file_path,
            }
        except Exception as e:
            logger.error(f"ImageKit upload exception: {str(e)}", exc_info=True)
            raise

    def delete_image(self, file_id: str) -> bool:
        """
        Delete an image from ImageKit.

        Args:
            file_id: The ImageKit file ID

        Returns:
            bool: True if deletion was successful
        """
        try:
            self.imagekit.delete_file(file_id=file_id)
            return True
        except Exception:
            return False

    def get_authentication_parameters(self) -> dict:
        """
        Get authentication parameters for client-side uploads.

        Returns:
            dict: Contains token, expire, and signature for client uploads
        """
        auth_params = self.imagekit.get_authentication_parameters()
        return {
            "token": auth_params["token"],
            "expire": auth_params["expire"],
            "signature": auth_params["signature"],
        }


# Singleton instance
imagekit_service = ImageKitService()
