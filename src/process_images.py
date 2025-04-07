"""
Process test images using the EnhancedImageDryer.
This script takes images from the test_images directory,
processes them with the EnhancedImageDryer, and saves the results
to the test_results directory.
"""

import os
import sys
import datetime
from PIL import Image
from pathlib import Path
from dotenv import load_dotenv

# Import the enhanced image dryer
from src.enhanced_image_dryer import EnhancedImageDryer

# Load environment variables
load_dotenv()

def process_image(image_path, use_fallback=False):
    """Process an image using the EnhancedImageDryer."""
    # Ensure test_results directory exists
    os.makedirs("test_results", exist_ok=True)
    
    # Load the image
    try:
        image = Image.open(image_path)
        print(f"Loaded image: {image_path}")
        print(f"Image size: {image.size}, Mode: {image.mode}")
    except Exception as e:
        print(f"Error loading image: {str(e)}")
        return False
    
    # Process the image with the EnhancedImageDryer
    print("Initializing EnhancedImageDryer...")
    dryer = EnhancedImageDryer()
    
    # Check if API key is set
    if not dryer.api_key:
        print("Error: STABILITY_API_KEY not found in environment variables.")
        print("Please set your Stability API key in the .env file.")
        return False
    
    print(f"API Key found: {dryer.api_key[:5]}...{dryer.api_key[-5:] if len(dryer.api_key) > 10 else ''}")
    
    if use_fallback:
        # Use the fallback method directly
        print("Using fallback drying method as requested...")
        processed_image = dryer.apply_fallback_drying_effect(image)
    else:
        # Try the API first
        print("Attempting to process with Stability AI API...")
        processed_image = dryer.process_image(image)
        
        # If API fails, use fallback method
        if processed_image is None:
            print("API processing failed. Using fallback drying method...")
            processed_image = dryer.apply_fallback_drying_effect(image)
    
    if processed_image:
        # Save the processed image
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"test_results/enhanced_dried_{Path(image_path).stem}_{timestamp}.png"
        processed_image.save(output_filename)
        print(f"Successfully processed image and saved to: {output_filename}")
        return True
    else:
        print(f"Failed to process image: {image_path}")
        return False

def main():
    """Main function to process images from the test_images directory."""
    print("\n=== Processing Test Images with EnhancedImageDryer ===\n")
    
    # Parse command line arguments
    use_fallback = "--fallback" in sys.argv
    if use_fallback:
        print("Fallback mode enabled: Will use local processing instead of API")
    
    # Check if test_images directory exists
    if not os.path.exists("test_images"):
        print("Error: test_images directory not found.")
        return
    
    # Get list of image files in the test_images directory
    image_files = [f for f in os.listdir("test_images") 
                  if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    
    if not image_files:
        print("No image files found in the test_images directory.")
        print("Please place your test images in the test_images directory.")
        return
    
    print(f"Found {len(image_files)} image(s) in the test_images directory:")
    for i, file in enumerate(image_files, 1):
        print(f"{i}. {file}")
    
    # Process each image
    print("\nProcessing images...")
    for file in image_files:
        image_path = os.path.join("test_images", file)
        print(f"\nProcessing: {file}")
        success = process_image(image_path, use_fallback)
        if success:
            print(f"[SUCCESS] Successfully processed {file}")
        else:
            print(f"[FAILED] Failed to process {file}")
    
    print("\nAll processing complete!")
    print(f"Processed images saved to the test_results directory.")

if __name__ == "__main__":
    main()
