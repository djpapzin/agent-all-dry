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

## Prerequisites

- Python 3.8 or higher
- OpenRouter API key
- Stability AI API key
- Virtual environment (recommended)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/L-fanampe/agent-all-dry.git
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

1. Start the application:
```bash
python -m src.app
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
├── src/                # Source code
├── tests/             # Test files
├── test_images/       # Sample images for testing
├── .env.example       # Environment variables template
├── requirements.txt   # Project dependencies
└── README.md         # Documentation
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

MIT License - See LICENSE file for details

## Author

DJ Papzin (L.fanampe@gmail.com) 