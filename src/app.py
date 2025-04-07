import os
import gradio as gr
from PIL import Image
from typing import Tuple, Optional
from dotenv import load_dotenv
from .drying_agent import DryingAgent

# Load environment variables
load_dotenv()

class DryingApp:
    def __init__(self):
        """Initialize the DryingApp with the agent and interface."""
        self.agent = DryingAgent()
        
    def process_interaction(
        self,
        message: str,
        image: Optional[Image.Image],
        history: list
    ) -> Tuple[list, Optional[Image.Image]]:
        """Process user interaction and update chat history."""
        # Get response from agent
        response, processed_image = self.agent.process_message(message, image)
        
        # Update history
        history.append((message, response))
        
        return history, processed_image
        
    def reset_conversation(self):
        """Reset the conversation and agent state."""
        self.agent.reset()
        return [], None
        
    def create_interface(self):
        """Create and configure the Gradio interface."""
        with gr.Blocks(title="Item Drying Assistant") as interface:
            gr.Markdown("# Item Drying Assistant")
            gr.Markdown("Upload an image of a wet item and I'll help you dry it!")
            
            with gr.Row():
                with gr.Column(scale=2):
                    chatbot = gr.Chatbot(
                        label="Chat History",
                        height=400,
                        type="messages"
                    )
                    message = gr.Textbox(
                        label="Your message",
                        placeholder="Type your message here...",
                        lines=2
                    )
                    with gr.Row():
                        submit = gr.Button("Send")
                        reset = gr.Button("Reset")
                        
                with gr.Column(scale=1):
                    image_input = gr.Image(
                        label="Upload Image",
                        type="pil"
                    )
                    image_output = gr.Image(
                        label="Processed Image",
                        type="pil"
                    )
            
            # Set up event handlers
            submit.click(
                fn=self.process_interaction,
                inputs=[message, image_input, chatbot],
                outputs=[chatbot, image_output],
                api_name="process"
            )
            
            reset.click(
                fn=self.reset_conversation,
                inputs=[],
                outputs=[chatbot, image_output],
                api_name="reset"
            )
            
        return interface

def main():
    """Main function to run the application."""
    app = DryingApp()
    interface = app.create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True
    )

if __name__ == "__main__":
    main() 