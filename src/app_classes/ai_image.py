from app_classes.base_app import BaseApp

IMAGE_MODELS = ["dall-e-3", "dall-e-2"]
DEFAULT_IMAGE_MODEL = "dall-e-3"

IMAGE_QUALITIES = ["hd", "standard"]
DEFAULT_IMAGE_QUALITY = "standard"
class AIImageApp(BaseApp):
    def generate_image(self, settings):
        text_prompt = settings.get("inputText")

        image_model = settings.get('imageModel', DEFAULT_IMAGE_MODEL)
        if image_model not in IMAGE_MODELS:
            image_model = DEFAULT_IMAGE_MODEL
        image_quality = settings.get('quality', DEFAULT_IMAGE_QUALITY)
        if image_quality not in IMAGE_QUALITIES:
            image_quality = DEFAULT_IMAGE_QUALITY
        randomize_prompt = settings.get('randomizePrompt') == 'true'
        if randomize_prompt:
            text_prompt = self.dependencies["openai_client"].get_image_prompt(text_prompt)

        image = self.dependencies["openai_client"].generate_image(
            text_prompt,
            model=image_model,
            quality=image_quality
        )
        return image