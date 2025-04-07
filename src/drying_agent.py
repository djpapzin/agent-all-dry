import os
from typing import Optional, Tuple, List, Union
from PIL import Image
# Import from langchain directly for better compatibility
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from src.image_dryer import ImageDryer

class DryingAgent:
    def __init__(self):
        """Initialize the DryingAgent with chat model and image processor."""
        self.chat_model = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            model_name="google/gemini-2.5-pro-exp-03-25:free",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            temperature=0.7
        )
        
        self.image_dryer = ImageDryer()
        self.chat_history: List[Union[HumanMessage, AIMessage]] = []
        self.current_image: Optional[Image.Image] = None
        self.processed_image: Optional[Image.Image] = None
        
        # System prompt for the agent
        self.system_prompt = SystemMessage(content="""You are a helpful assistant specialized in drying items. 
        Your main task is to help users dry various items and provide advice about drying processes. 
        When users provide images, you should analyze them and suggest appropriate drying methods. 
        Always maintain a professional and helpful tone while focusing on drying-related queries.""")
    
    def process_message(self, message: str, image: Optional[Image.Image] = None) -> Tuple[list, Optional[Image.Image]]:
        """Process a user message and optional image, return response and processed image."""
        try:
            self.current_image = image
            
            # Create message history for the chat model
            messages = [self.system_prompt] + self.chat_history + [HumanMessage(content=message)]
            
            # Get response from chat model
            response = self.chat_model.predict_messages(messages)
            
            # Process image if provided
            if image is not None:
                self.processed_image = self.image_dryer.process_image(image)
            else:
                self.processed_image = None
            
            # Update chat history
            self.chat_history.append(HumanMessage(content=message))
            self.chat_history.append(AIMessage(content=response.content))
            
            # Return messages in Gradio chatbot format
            return [
                {"role": "user", "content": message},
                {"role": "assistant", "content": response.content}
            ], self.processed_image
            
        except Exception as e:
            print(f"Error in process_message: {str(e)}")
            return [{"role": "assistant", "content": f"Error: {str(e)}"}], None
    
    def reset(self):
        """Reset the agent's state."""
        self.chat_history = []
        self.current_image = None
        self.processed_image = None 