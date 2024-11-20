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
    
    def generate_image(self, prompt, image_dir, test=True):
        print(f"Generating image for prompt: {prompt}")
        args = {
            "model": "dall-e-2",
            "prompt": prompt,
            "size": "1024x1024"
        }
        if not test:
            args["model"] = "dall-e-3"
            args["size"] = "1792x1024"
            args["quality"] = "hd"
        response = self.ai_client.images.generate(**args)
        image_url = response.data[0].url
        print(f"Saving file to {image_dir}")
        urllib.request.urlretrieve(image_url, image_dir)
    
    def get_image_prompt(self):
        print(f"Getting random image prompt.")

        # Make the API call
        response = self.ai_client.Completion.create(
            model="gpt-4o-mini",  # Specify the model
            messages=[
                {"role": "system", "content": "You are a creative assistant generating unique image prompts."},
                {"role": "user", "content": "Generate a random, creative, and vivid description for an image prompt."}
            ],
            temperature=0.8,  # Adjust for creativity
            max_tokens=50
        )
        
        prompt = response.choices[0].message['content'].strip()
        print(f"Generated random image prompt: {prompt}")
        return prompt
