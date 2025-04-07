# Drying Assistant

An AI-powered assistant that helps you understand how to dry different items and shows you what they would look like when dry. Built with Gradio and powered by LangChain and Stability AI.

## Features

- 🤖 Intelligent chat interface for asking questions about drying items
- 🖼️ Image upload and processing to show dried appearance
- 🎨 Realistic image transformation using Stability AI API
- 💬 Context-aware conversations with memory
- 🎯 User-friendly interface with Gradio

## Application Screenshot

![Drying Assistant Interface](app_screenshot.png)

*The Drying Assistant web interface showing the chat and image processing capabilities.*

## Usage

1. Upload images using the file upload component
2. Type your questions in the chat interface
3. View the processed images showing dried appearance
4. Use the reset button to start a new conversation
5. Download processed images using the download button

## Important Note

This application requires API keys to function properly:
- OPENROUTER_API_KEY for the chat functionality
- STABILITY_API_KEY for image processing

Please set these environment variables in your Hugging Face Space settings.

## Author

DJ Papzin (L.fanampe@gmail.com)
