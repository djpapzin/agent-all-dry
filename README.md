# Drying Assistant

An AI-powered assistant that helps you understand how to dry different items and shows you what they would look like when dry. Built with Gradio and powered by LangChain and Stability AI.

## Features

- 🤖 Intelligent chat interface for asking questions about drying items
- 🖼️ Image upload and processing to show dried appearance
- 🎨 Realistic image transformation using Stability AI API
- 💬 Context-aware conversations with memory
- 🎯 User-friendly interface with Gradio
- 🔄 Real-time image processing
- 📱 Responsive design for all devices
- 🐳 Docker support for easy deployment

## Live Demo: https://drying-assistant.onrender.com

![Drying Assistant Interface](app_screenshot.png)


*The Drying Assistant web interface showing the chat and image processing capabilities.*

## Prerequisites

- Python 3.8 or higher
- OpenRouter API key
- Stability AI API key
- Docker and Docker Compose (optional, for containerized deployment)
- Virtual environment (for local development)

## Deployment Options

### 1. Docker Deployment (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/djpapzin/agent-all-dry.git
cd agent-all-dry
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

3. Build and run with Docker Compose:
```bash
docker-compose up -d
```

The application will be available at `http://localhost:7860`

To stop the application:
```bash
docker-compose down
```

### 2. Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/djpapzin/agent-all-dry.git
cd agent-all-dry
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/MacOS
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. Run the application:
```bash
python -m src.app
```

The application will be available at `http://localhost:7860`

## Setup

1. Clone the repository:
```bash
git clone https://github.com/djpapzin/agent-all-dry.git
cd agent-all-dry
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/MacOS
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
OPENROUTER_API_KEY=your_api_key_here
STABILITY_API_KEY=your_api_key_here
```

## Usage

### Running the Web Application

1. Start the application using the run script:
```bash
python run.py
```

2. Open your browser and navigate to:
```
http://localhost:7860
```

3. Using the interface:
   - Upload images using the file upload component
   - Type your questions in the chat interface
   - View the processed images showing dried appearance
   - Use the reset button to start a new conversation
   - Download processed images using the download button

### Processing Test Images

You can process test images using the enhanced image dryer without starting the web application:

```bash
# Process images using Stability AI API
python -m src.process_images

# Process images using local fallback method (no API call)
python -m src.process_images --fallback

# Alternative processing tool
python -m src.tools.process_with_enhanced_dryer
```

Processed images will be saved to the `test_results` directory.

## Test Images

The repository includes sample images in the `test_images` directory that you can use to test the application:

1. Tomato Image:
   - File: `test_images/tomato.jpg`
   - Try prompt: "This is a whole medium-sized red tomato. Make it sun-dried on a medium level."

2. Kitten Image:
   - File: `test_images/kitten.jpg`
   - Try prompt: "This is a tiny kitten. Please dry it and make it completely dehydrated."

Feel free to experiment with your own images and prompts!

## Development

### Project Structure
```
.
├── src/                # Source code directory
│   ├── __init__.py
│   ├── app.py           # Main application
│   ├── chat_model.py    # Chat model implementation
│   ├── drying_agent.py  # Drying agent implementation
│   ├── enhanced_image_dryer.py  # Enhanced image processing
│   ├── image_dryer.py   # Image drying implementation
│   ├── process_images.py  # Image processing script
│   └── tools/           # Utility tools
│       └── process_with_enhanced_dryer.py  # Enhanced image processing tool
├── tests/               # Test directory
│   ├── test_drying_agent.py
│   └── test_drying_assistant.py
├── test_images/         # Sample images for testing
│   ├── kitten.jpg
│   └── tomato.jpg
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore file
├── requirements.txt     # Project dependencies
├── run.py              # Application launcher script
├── setup.py            # Python package configuration
├── LICENSE             # MIT License file
└── README.md           # Documentation
```

### Running Tests
```bash
# Run all tests
pytest tests/

# Run tests with coverage
pytest --cov=src tests/
```

### Code Quality
```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Sort imports
isort src/ tests/
```

## Dependencies

- langchain: For AI conversation handling
- gradio: For the web interface
- stability-sdk: For image processing via API
- python-dotenv: For environment variable management
- pytest: For testing
- pillow: For image processing
- black, flake8, isort: For code quality

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.

## Author

DJ Papzin (L.fanampe@gmail.com) 