import os
from typing import Optional
from PIL import Image
import io
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

class ImageDryer:
    def __init__(self):
        """Initialize the ImageDryer with Stability AI API."""
        self.api_key = os.getenv("STABILITY_API_KEY")
        self.api_host = "https://api.stability.ai"
        self.engine_id = "stable-diffusion-xl-1024-v1-0"
        
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """Preprocess the image to meet API requirements."""
        # Convert to RGB if needed
        if image.mode != "RGB":
            image = image.convert("RGB")
            
        # Resize if larger than 1024x1024
        max_size = 1024
        if max(image.size) > max_size:
            ratio = max_size / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            image = image.resize(new_size, Image.LANCZOS)
            
        return image
        
    def process_image(self, image: Image.Image) -> Optional[Image.Image]:
        """Process an image to make it appear dry using Stability AI API."""
        try:
            # Preprocess the image
            processed_image = self.preprocess_image(image)
            
            # Convert image to bytes
            buffered = io.BytesIO()
            processed_image.save(buffered, format="PNG")
            img_bytes = buffered.getvalue()
            
            # Prepare the API request
            url = f"{self.api_host}/v1/generation/{self.engine_id}/image-to-image"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            files = {
                "init_image": ("image.png", img_bytes, "image/png"),
            }
            
            data = {
                "image_strength": 0.35,
                "text_prompts[0][text]": "A completely dry version of this item, photorealistic, detailed texture, no water or moisture",
                "text_prompts[0][weight]": 1,
                "text_prompts[1][text]": "wet, moist, damp, water droplets, puddles, stains",
                "text_prompts[1][weight]": -1,
                "cfg_scale": 7,
                "samples": 1,
                "steps": 30
            }
            
            # Make the API request
            response = requests.post(url, headers=headers, files=files, data=data)
            
            if response.status_code != 200:
                raise Exception(f"API request failed: {response.text}")
            
            # Process the response
            data = response.json()
            image_data = base64.b64decode(data["artifacts"][0]["base64"])
            
            # Convert to PIL Image
            result = Image.open(io.BytesIO(image_data))
            return result
            
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return None

    def save_image(self, image: Image.Image, filename: str) -> None:
        """Save an image to a file."""
        image.save(filename)

    def image_to_bytes(self, image: Image.Image) -> bytes:
        """Convert PIL Image to bytes."""
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue() 