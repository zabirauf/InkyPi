from apps.base_app.base_app import BaseApp
from PIL import Image
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

class ImageUploadApp(BaseApp):
    def generate_image(self, settings, device_config):
        image_location = settings.get("imageFile")

        if not image_location:
            raise RuntimeError("Image not provided.")
        # Open the image using Pillow
        try:
            image = Image.open(image_location)
        except Exception as e:
            logger.error(f"Failed to read image file: {str(e)}")
            raise RuntimeError("Failed to read image file.")

        return image