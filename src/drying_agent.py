import os
from typing import Optional, Tuple, List, Union
from PIL import Image
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from .image_dryer import ImageDryer

class DryingAgent:
    def __init__(self):
        """Initialize the DryingAgent with chat model and image processor."""
        self.chat_model = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            model_name="google/gemini-pro",
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
            if not message or not isinstance(message, str):
                raise ValueError("Message must be a non-empty string")
            
            self.current_image = image
            messages = [self.system_prompt] + self.chat_history + [HumanMessage(content=message)]
            
            response = self.chat_model.invoke(messages)
            response_content = response.content if hasattr(response, 'content') else str(response)
            
            if image is not None:
                self.processed_image = self.image_dryer.process_image(image)
            else:
                self.processed_image = None
            
            self.chat_history.append(HumanMessage(content=message))
            self.chat_history.append(AIMessage(content=response_content))
            
            if len(self.chat_history) > 20:
                self.chat_history = self.chat_history[-20:]
            
            return [
                {"role": "user", "content": message},
                {"role": "assistant", "content": response_content}
            ], self.processed_image
            
        except ValueError as ve:
            return [{"role": "assistant", "content": f"Invalid input: {str(ve)}"}], None
        except Exception as e:
            print(f"Error in process_message: {str(e)}")
            return [{"role": "assistant", "content": f"An error occurred: {str(e)}"}], None
    
    def reset(self):
        """Reset the agent's state."""
        self.chat_history = []
        self.current_image = None
        self.processed_image = None 