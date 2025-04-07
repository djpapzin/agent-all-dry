from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

class ChatModel:
    def __init__(self):
        load_dotenv()
        self.model = ChatOpenAI(
            model_name="google/gemini-2.0-flash-lite-preview-02-05:free",
            openai_api_base="https://openrouter.ai/api/v1",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            temperature=0.7,
        )
        
        self.system_prompt = """You are a helpful assistant focused on drying items. 
        Your role is to help users understand how to dry different items and show them 
        what items would look like when dry. You should:
        1. Ask for item descriptions if not provided
        2. Only process drying-related requests
        3. Maintain conversation context
        4. Be helpful and informative about drying processes
        """

    def get_response(self, message: str, chat_history: list = None) -> str:
        """
        Get a response from the chat model.
        
        Args:
            message: User's message
            chat_history: List of previous messages (optional)
            
        Returns:
            Model's response
        """
        messages = [SystemMessage(content=self.system_prompt)]
        
        if chat_history:
            for msg in chat_history:
                messages.append(HumanMessage(content=msg))
        
        messages.append(HumanMessage(content=message))
        
        response = self.model(messages)
        return response.content 