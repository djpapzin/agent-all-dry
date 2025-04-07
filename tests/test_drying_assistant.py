import pytest
import os
from unittest.mock import patch, MagicMock
from PIL import Image
from src.drying_agent import DryingAgent
from src.image_dryer import ImageDryer
from src.chat_model import ChatModel
from langchain.schema import AIMessage

# Set mock environment variables for testing
os.environ['OPENROUTER_API_KEY'] = 'test_api_key'

@pytest.fixture
def mock_stable_diffusion():
    # Use direct patching without importing the module
    patcher = patch('src.image_dryer.StableDiffusionImg2ImgPipeline', create=True)
    mock = patcher.start()
    mock_instance = MagicMock()
    mock.from_pretrained.return_value = mock_instance
    mock_instance.return_value = MagicMock(spec=Image.Image)
    yield mock
    patcher.stop()

@pytest.fixture
def mock_chat_model():
    with patch('src.drying_agent.ChatOpenAI') as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        mock_instance.predict_messages.return_value = AIMessage(content="Test response")
        yield mock_instance

@pytest.fixture
def mock_image_dryer(mock_stable_diffusion):
    # Use direct import path to match the agent's import
    with patch('src.drying_agent.ImageDryer') as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        mock_instance.process_image.return_value = MagicMock(spec=Image.Image)
        yield mock

def test_drying_agent_initialization(mock_chat_model, mock_image_dryer):
    """Test that the DryingAgent initializes correctly."""
    agent = DryingAgent()
    assert isinstance(agent, DryingAgent)
    assert agent.chat_model is not None
    assert agent.image_dryer is not None

def test_process_message(mock_chat_model, mock_image_dryer):
    """Test processing a message without an image."""
    agent = DryingAgent()
    response, processed_image = agent.process_message("test message")
    assert isinstance(response, str)
    assert processed_image is None
    assert len(agent.chat_history) == 2  # Human message and AI response

def test_process_message_with_image(mock_chat_model, mock_image_dryer):
    """Test processing a message with an image."""
    agent = DryingAgent()
    test_image = MagicMock(spec=Image.Image)
    response, processed_image = agent.process_message("test message", test_image)
    assert isinstance(response, str)
    assert processed_image is not None
    mock_image_dryer.return_value.process_image.assert_called_once_with(test_image)

def test_chat_history(mock_chat_model, mock_image_dryer):
    """Test chat history management."""
    agent = DryingAgent()
    agent.process_message("test message")
    assert len(agent.chat_history) == 2  # Human message and AI response

def test_reset(mock_chat_model, mock_image_dryer):
    """Test resetting the agent state."""
    agent = DryingAgent()
    agent.process_message("test message")
    agent.reset()
    assert len(agent.chat_history) == 0
    assert agent.current_image is None
    assert agent.processed_image is None