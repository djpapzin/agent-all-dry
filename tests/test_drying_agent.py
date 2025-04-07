import pytest
from unittest.mock import MagicMock, patch
from PIL import Image
from src.drying_agent import DryingAgent
from langchain.schema import AIMessage, HumanMessage, SystemMessage

@pytest.fixture
def mock_chat_model():
    with patch('src.drying_agent.ChatOpenAI') as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        mock_instance.predict_messages.return_value = AIMessage(content="Test response")
        yield mock_instance

@pytest.fixture
def mock_image_dryer():
    with patch('src.drying_agent.ImageDryer') as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        mock_instance.process_image.return_value = MagicMock(spec=Image.Image)
        yield mock_instance

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
    mock_image_dryer.process_image.assert_called_once_with(test_image)

def test_chat_history(mock_chat_model, mock_image_dryer):
    """Test chat history maintenance."""
    agent = DryingAgent()
    messages = [
        "How do I dry a wet towel?",
        "What about a wet carpet?",
        "And a wet book?"
    ]

    for message in messages:
        response, _ = agent.process_message(message)
        assert isinstance(response, str)

    assert len(agent.chat_history) == len(messages) * 2  # Each message has a response

def test_reset(mock_chat_model, mock_image_dryer):
    """Test resetting the agent state."""
    agent = DryingAgent()
    agent.process_message("test message")
    agent.reset()
    
    assert len(agent.chat_history) == 0
    assert agent.current_image is None
    assert agent.processed_image is None 