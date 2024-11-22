import urllib.request
from dotenv import load_dotenv
from openai import OpenAI
import traceback
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
        try:
            prompt += ".Ensure the images are optimized for a 7-color e-ink display, focusing on simplicity, contrast, and bold shapes to ensure readability and vibrancy on limited palettes."
            args = {
                "model": "dall-e-2",
                "prompt": prompt,
                "size": "1024x1024"
            }
            if not test:
                args["model"] = "dall-e-3"
                args["size"] = "1792x1024"
                args["quality"] = "standard"
            response = self.ai_client.images.generate(**args)
            image_url = response.data[0].url
            print(f"Saving file to {image_dir}")
            urllib.request.urlretrieve(image_url, image_dir)
        except Exception as e:
            print("Failed to generate an image:")
            print(traceback.format_exc())
    
    def get_image_prompt(self):
        print(f"Getting random image prompt...")

        # Make the API call
        response = self.ai_client.chat.completions.create(
            model="gpt-4o",  # Specify the model
            messages=[
                {
                    "role": "system",
                    "content": "You are a creative assistant generating extremely random and unique image prompts. Avoid common themes. Focus on unexpected, unconventional, and bizarre combinations of art style, medium, subjects, time periods, and moods. No repetition. Prompts should be 10 words or less and specify random artist, movie, tv show or time period for the theme."},
                {
                    "role": "user",
                    "content": "Give me a completely random image prompt, something unexpected and creative! Let's see what your AI mind can cook up! "}
            ],
            # frequency_penalty=2,
            # presence_penalty=2,
            temperature=1,  # Adjust for creativity
            max_tokens=50
        )

        prompt = response.choices[0].message.content.strip()
        #print(f"Generated random image prompt: {prompt}")
        return prompt
