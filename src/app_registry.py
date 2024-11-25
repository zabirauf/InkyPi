# app_registry.py

from app_classes.ai_image import AIImageApp
from app_classes.image_upload import ImageUploadApp
from clients.openai import OpenAIClient

# Shared clients and dependencies
openai_client = OpenAIClient()

# Shared app instances (singleton pattern)
app_instances = {
    "AI Image": AIImageApp(openai_client=openai_client),
    "Image Upload": ImageUploadApp(),
}

def get_app_instance(app_name):
    return app_instances.get(app_name)
