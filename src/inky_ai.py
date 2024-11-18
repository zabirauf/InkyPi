import urllib.request
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

class InkyAI:

    def __init__(self):
        print("Instantiating Open AI client.")
        api_key = os.getenv("OPEN_AI_SECRET")
        self.ai_client = OpenAI(
            api_key = api_key
        )
    
    def generate_image(self, prompt, image_dir):
        print(f"Generating image for prompt: {prompt}")
        response = self.ai_client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="1024x1024"
        )
        image_url = response.data[0].url
        print(image_url)
        urllib.request.urlretrieve(image_url, image_dir)
