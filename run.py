"""
Run script for the Drying Assistant application.
This script provides a convenient way to start the application.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_api_keys():
    """Check if the required API keys are set."""
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    stability_key = os.getenv("STABILITY_API_KEY")
    
    if not openrouter_key:
        print("Warning: OPENROUTER_API_KEY is not set in your .env file.")
        print("Chat functionality may not work properly.")
    else:
        print(f"[OK] OpenRouter API key found: {openrouter_key[:5]}...{openrouter_key[-5:] if len(openrouter_key) > 10 else ''}")
    
    if not stability_key:
        print("Warning: STABILITY_API_KEY is not set in your .env file.")
        print("Image drying functionality may not work properly.")
    else:
        print(f"[OK] Stability AI API key found: {stability_key[:5]}...{stability_key[-5:] if len(stability_key) > 10 else ''}")
    
    return openrouter_key and stability_key

def main():
    """Main function to run the Drying Assistant application."""
    print("\n=== Drying Assistant by DJ Papzin ===\n")
    
    # Check API keys
    keys_ok = check_api_keys()
    if not keys_ok:
        print("\nSome API keys are missing. The application may not function properly.")
        response = input("Do you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Exiting. Please set up your API keys in the .env file and try again.")
            sys.exit(1)
    
    # Import here to avoid circular imports
    from src.app import DryingApp, main as app_main
    
    print("\nStarting Drying Assistant application...")
    print("The web interface will be available at http://localhost:7860")
    print("Press Ctrl+C to stop the application.")
    
    # Run the app using the main function from app.py
    app_main()

if __name__ == "__main__":
    main()
