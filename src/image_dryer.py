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
        try:
            # Convert to RGB if needed
            if image.mode != "RGB":
                image = image.convert("RGB")
                
            # Get current dimensions
            width, height = image.size
            
            # Calculate aspect ratio
            aspect_ratio = width / height
            
            # Define supported dimensions
            supported_dimensions = [
                (1024, 1024),  # 1:1
                (1152, 896),   # 1.29:1
                (1216, 832),   # 1.46:1
                (1344, 768),   # 1.75:1
                (1536, 640),   # 2.4:1
                (640, 1536),   # 1:2.4
                (768, 1344),   # 1:1.75
                (832, 1216),   # 1:1.46
                (896, 1152)    # 1:1.29
            ]
            
            # Find the closest aspect ratio
            target_dims = min(supported_dimensions, 
                            key=lambda dims: abs((dims[0]/dims[1]) - aspect_ratio))
            
            # Print debug info
            print(f"Original dimensions: {width}x{height}, aspect ratio: {aspect_ratio:.2f}")
            print(f"Selected target dimensions: {target_dims[0]}x{target_dims[1]}")
            
            # Resize image to target dimensions using high-quality resampling
            image = image.resize(target_dims, Image.Resampling.LANCZOS)
            
            # Verify final dimensions
            final_width, final_height = image.size
            if (final_width, final_height) not in supported_dimensions:
                raise ValueError(f"Failed to resize to supported dimensions. Got {final_width}x{final_height}")
                
            return image
            
        except Exception as e:
            print(f"Error in preprocess_image: {str(e)}")
            raise
        
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