import urllib.request
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
import traceback
import requests
import os
from io import BytesIO

load_dotenv()

class OpenAIClient:

    def __init__(self):
        print("Instantiating Open AI client.")
        api_key = os.getenv("OPEN_AI_SECRET")
        self.ai_client = OpenAI(
            api_key = api_key
        )
    
    def generate_image(self, prompt, model="dalle-e-3", quality="standard"):
        print(f"Generating image for prompt: {prompt}, model: {model}, quality: {quality}")
        img = None
        try:
            prompt += (
                ". The image should fully occupy the entire canvas without any frames, "
                "borders, or cropped areas. No blank spaces or artificial framing."
            )
            prompt += (
                "Focus on simplicity, bold shapes, and strong contrast to enhance clarity "
                "and visual appeal. Avoid excessive detail or complex gradients, ensuring "
                "the design works well with flat, vibrant colors."
            )
            args = {
                "model": model,
                "prompt": prompt,
                "size": "1024x1024",
                "quality": "standard"
            }
            if model == "dall-e-3":
                args["size"] = "1792x1024"
                args["quality"] = quality
            print("OPENAI API ARGS: " + str(args))
            response = self.ai_client.images.generate(**args)
            image_url = response.data[0].url
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
        except Exception as e:
            print("Failed to generate an image:")
            print(traceback.format_exc())
        return img
    
    def get_image_prompt(self, from_prompt=None):
        print(f"Getting random image prompt...")

        system_content = (
            "You are a creative assistant generating extremely random and unique image prompts. "
            "Avoid common themes. Focus on unexpected, unconventional, and bizarre combinations "
            "of art style, medium, subjects, time periods, and moods. No repetition. Prompts "
            "should be 20 words or less and specify random artist, movie, tv show or time period "
            "for the theme. Do not provide any headers or repeat the request, just provide the updated "
            "updated prompt in your response."
        )
        user_content = (
            "Give me a completely random image prompt, something unexpected and creative! "
            "Let's see what your AI mind can cook up!"
        )
        if from_prompt and from_prompt.strip():
            system_content = (
                "You are a creative assistant specializing in generating highly descriptive "
                "and unique prompts for creating images. When given a short or simple image "
                "description, your job is to rewrite it into a more detailed, imaginative, "
                "and descriptive version that captures the essence of the original while "
                "making it unique and vivid. Avoid adding irrelevant details but feel free "
                "to include creative and visual enhancements. Avoid common themes. Focus on "
                "unexpected, unconventional, and bizarre combinations of art style, medium, "
                "subjects, time periods, and moods. Do not provide any headers or repeat the "
                "request, just provide your updated prompt in the response. Prompts "
                "should be 20 words or less and specify random artist, movie, tv show or time "
                "period for the theme."
            )
            user_content = (
                f"Original prompt: \"{from_prompt}\"\n"
                "Rewrite it to make it more detailed, imaginative, and unique while staying "
                "true to the original idea. Include vivid imagery and descriptive details. "
                "Avoid changing the subject of the prompt."
            )
    

        # Make the API call
        response = self.ai_client.chat.completions.create(
            model="gpt-4o",  # Specify the model
            messages=[
                {
                    "role": "system",
                    "content": system_content
                },
                {
                    "role": "user",
                    "content": user_content
                }
            ],
            # frequency_penalty=2,
            # presence_penalty=2,
            temperature=1,  # Adjust for creativity
            max_tokens=50
        )

        prompt = response.choices[0].message.content.strip()
        print(f"Generated random image prompt: {prompt}")
        return prompt
