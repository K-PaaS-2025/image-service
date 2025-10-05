import logging
import io
from typing import Optional, Tuple

from ..data import storage
from ..model import openai_client

logger = logging.getLogger(__name__)

def generate_letter_with_image(image_data: bytes, filename: str) -> Optional[Tuple[str, str]]:
    try:
        # generate object key for storage
        object_key = f"images/{filename}"
        logger.info(f"Processing image: {filename}")

        # upload image to NCloud Object Storage
        file_obj = io.BytesIO(image_data)
        image_url = storage.upload_fileobj(file_obj, object_key)

        if not image_url:
            logger.error("Failed to upload image to NCloud storage")
            return None

        logger.info(f"Image uploaded successfully: {image_url}")

        # generate letter using the uploaded image URL
        letter = openai_client.generate_letter(image_url)

        if not letter:
            logger.error("Failed to generate letter from image")
            return None

        logger.info(f"Letter generated successfully for {filename}")

        # return both image URL and generated letter
        return (image_url, letter)

    except Exception as e:
        logger.error(f"Failed to process image and generate letter: {e}")
        return None