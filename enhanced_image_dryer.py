"""
Enhanced ImageDryer with better error handling and alternative API options.
This module provides a more robust implementation of the ImageDryer class
with improved error handling, retry logic, and alternative API endpoints.
"""

import os
import time
import io
import base64
import requests
import random
from typing import Optional, List, Dict, Any
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EnhancedImageDryer:
    def __init__(self):
        """Initialize the EnhancedImageDryer with Stability AI API."""
        self.api_key = os.getenv("STABILITY_API_KEY")
        self.api_host = "https://api.stability.ai"
        # List of available engines to try
        self.engines = [
            "stable-diffusion-xl-1024-v1-0",
            "stable-diffusion-v1-5",
            "stable-diffusion-512-v2-1"
        ]
        self.current_engine = self.engines[0]
        self.max_retries = 3
        self.retry_delay = 2  # seconds between retries
        
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
    
    def get_prompt_variations(self) -> List[Dict[str, Any]]:
        """Get different prompt variations to try for better results."""
        prompt_variations = [
            # Standard drying prompt
            [
                {
                    "text": "A completely dry version of this item, photorealistic, detailed texture, no water or moisture",
                    "weight": 1
                },
                {
                    "text": "wet, moist, damp, water droplets, puddles, stains",
                    "weight": -1
                }
            ],
            # Alternative drying prompt with more emphasis on dryness
            [
                {
                    "text": "Bone dry, completely dried out, arid, desert-like dryness, crisp texture, no moisture whatsoever",
                    "weight": 1
                },
                {
                    "text": "wet, damp, moist, humidity, water, liquid, droplets, condensation",
                    "weight": -1
                }
            ],
            # Focus on texture and detail
            [
                {
                    "text": "Dry texture, detailed fabric, no moisture, sun-dried appearance, crisp details",
                    "weight": 1
                },
                {
                    "text": "wet appearance, water stains, dampness, moisture",
                    "weight": -1
                }
            ]
        ]
        return prompt_variations
    
    def process_image(self, image: Image.Image) -> Optional[Image.Image]:
        """Process an image to make it appear dry using Stability AI API with robust error handling."""
        if not self.api_key:
            print("Error: No Stability API key found in environment variables.")
            return None
            
        # Preprocess the image
        processed_image = self.preprocess_image(image)
        
        # Convert image to base64
        buffered = io.BytesIO()
        processed_image.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        # Try different engines and prompts
        prompt_variations = self.get_prompt_variations()
        
        for retry in range(self.max_retries):
            # Select engine based on retry count
            self.current_engine = self.engines[retry % len(self.engines)]
            
            # Select prompt variation
            prompts = prompt_variations[retry % len(prompt_variations)]
            
            print(f"Attempt {retry+1}/{self.max_retries} using engine: {self.current_engine}")
            
            try:
                # Prepare the API request
                url = f"{self.api_host}/v1/generation/{self.current_engine}/image-to-image"
                
                headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }
                
                # Adjust parameters based on the engine
                image_strength = 0.35
                cfg_scale = 7
                steps = 30
                
                if "xl" not in self.current_engine:
                    # Adjust parameters for non-XL models
                    image_strength = 0.4
                    cfg_scale = 8
                    steps = 25
                
                body = {
                    "image_strength": image_strength,
                    "init_image": img_base64,
                    "text_prompts": prompts,
                    "cfg_scale": cfg_scale,
                    "samples": 1,
                    "steps": steps
                }
                
                # Make the API request
                print(f"Sending request to Stability AI API...")
                response = requests.post(url, headers=headers, json=body, timeout=60)
                
                if response.status_code == 200:
                    # Process the response
                    data = response.json()
                    image_data = base64.b64decode(data["artifacts"][0]["base64"])
                    
                    # Convert to PIL Image
                    result = Image.open(io.BytesIO(image_data))
                    print(f"Successfully processed image with engine: {self.current_engine}")
                    return result
                else:
                    print(f"API request failed with status code {response.status_code}: {response.text}")
                    
                    # Check for rate limiting or server errors
                    if response.status_code == 429:  # Too Many Requests
                        print("Rate limited. Waiting longer before retry...")
                        time.sleep(self.retry_delay * 3)  # Wait longer for rate limiting
                    elif response.status_code >= 500:  # Server errors
                        print("Server error. Retrying with different engine...")
                    else:
                        print(f"Error: {response.text}")
                        
            except Exception as e:
                print(f"Error during API request: {str(e)}")
            
            # Wait before retrying
            if retry < self.max_retries - 1:
                delay = self.retry_delay * (retry + 1)  # Increase delay with each retry
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
        
        print("All retry attempts failed.")
        return None
        
    def save_image(self, image: Image.Image, filename: str) -> None:
        """Save an image to a file."""
        image.save(filename)
        
    def image_to_bytes(self, image: Image.Image) -> bytes:
        """Convert PIL Image to bytes."""
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
        
    def apply_fallback_drying_effect(self, image: Image.Image) -> Image.Image:
        """Apply a simple drying effect as a fallback when API fails."""
        print("Applying fallback drying effect...")
        
        # Convert to RGB if not already
        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        # Create a copy to work with
        result = image.copy()
        
        # Apply brightness and contrast adjustments to simulate drying
        brightness_factor = 1.2
        contrast_factor = 1.1
        saturation_reduction = 0.8
        
        # Apply adjustments
        # 1. Increase brightness
        result = result.point(lambda p: min(255, int(p * brightness_factor)))
        
        # 2. Increase contrast
        result = result.point(lambda p: min(255, int(128 + contrast_factor * (p - 128))))
        
        # 3. Convert to HSV to reduce saturation
        from colorsys import rgb_to_hsv, hsv_to_rgb
        
        # Process each pixel
        width, height = result.size
        for x in range(width):
            for y in range(height):
                r, g, b = result.getpixel((x, y))
                h, s, v = rgb_to_hsv(r/255, g/255, b/255)
                s *= saturation_reduction  # Reduce saturation
                r, g, b = hsv_to_rgb(h, s, v)
                result.putpixel((x, y), (int(r*255), int(g*255), int(b*255)))
        
        return result
