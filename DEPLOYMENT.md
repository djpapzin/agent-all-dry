# Deployment Guide for Drying Assistant

This guide explains how to deploy the Drying Assistant application to Hugging Face Spaces.

## Prerequisites

1. A Hugging Face account (sign up at [huggingface.co](https://huggingface.co/join))
2. Your OpenRouter API key
3. Your Stability AI API key

## Deployment Steps

### 1. Create a New Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Fill in the following details:
   - Owner: Your username
   - Space name: drying-assistant (or any name you prefer)
   - License: MIT
   - SDK: Gradio
   - Space hardware: CPU (Free)
   - Make sure "Public" is selected

### 2. Upload Your Code

You have two options:

#### Option A: Using the Hugging Face Web Interface

1. Click on "Files" in your new Space
2. Upload all the files from your local repository

#### Option B: Using Git (Recommended)

1. Clone your Space repository:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/drying-assistant
   ```
2. Copy your project files to the cloned repository
3. Commit and push the changes:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push
   ```

### 3. Set Up Environment Variables (IMPORTANT)

To protect your API keys, set them as environment variables in your Space:

1. Go to your Space settings
2. Click on "Repository secrets"
3. Add the following secrets:
   - OPENROUTER_API_KEY: Your OpenRouter API key
   - STABILITY_API_KEY: Your Stability AI API key

### 4. Verify Deployment

1. Wait for the build to complete (this may take a few minutes)
2. Once deployed, your app will be available at:
   ```
   https://huggingface.co/spaces/YOUR_USERNAME/drying-assistant
   ```

## Troubleshooting

If you encounter any issues:

1. Check the build logs in your Space
2. Verify that your environment variables are correctly set
3. Ensure all dependencies are properly listed in requirements.txt

## Additional Deployment Options

### Deploying to Gradio Cloud

Gradio also offers its own hosting service:

1. Install the Gradio CLI:
   ```bash
   pip install gradio
   ```
2. Deploy your app:
   ```bash
   gradio deploy
   ```

### Deploying to Render

[Render](https://render.com/) is another good option for deploying Gradio apps:

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `python app.py`
5. Add your environment variables in the Render dashboard

Remember to never commit your API keys to the repository. Always use environment variables or secrets management for sensitive information.
