from app_classes.base_app import BaseApp

class ImageUploadApp(BaseApp):
    def generate_image(self, settings):
        file = settings.get("file")
        return self.file_upload_service.process_upload(file)