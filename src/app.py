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
        if not message.strip():
            return history, None
            
        try:
            # Get response from agent
            messages, processed_image = self.agent.process_message(message, image)
            
            # Update history with proper message format
            if not history:
                history = []
                
            # Safely extract the assistant's response
            assistant_response = messages[1]["content"] if len(messages) > 1 else "I apologize, but I couldn't process your message."
            
            history.extend([
                {"role": "user", "content": message},
                {"role": "assistant", "content": assistant_response}
            ])
            
            return history, processed_image
        except Exception as e:
            print(f"Error in process_interaction: {str(e)}")
            if not history:
                history = []
            history.append({"role": "assistant", "content": f"Error: {str(e)}"})
            return history, None
        
    def reset_conversation(self):
        """Reset the conversation and agent state."""
        self.agent.reset()
        return [], None
        
    def create_interface(self):
        """Create and configure the Gradio interface."""
        with gr.Blocks(
            title="Item Drying Assistant",
            theme=gr.themes.Soft(
                primary_hue="blue",
                secondary_hue="gray"
            ),
            css=".gradio-container {max-width: 1200px; margin: auto;}"
        ) as interface:
            gr.Markdown("# Item Drying Assistant")
            gr.Markdown("Upload an image of a wet item and I'll help you dry it!")
            
            with gr.Row():
                with gr.Column(scale=2):
                    chatbot = gr.Chatbot(
                        label="Chat History",
                        height=400,
                        type="messages",
                        show_label=True,
                        layout="bubble",
                        rtl=False,
                        show_copy_button=True
                    )
                    with gr.Row():
                        message = gr.Textbox(
                            label="Your message",
                            placeholder="Type your message here...",
                            lines=2,
                            max_lines=10,
                            show_label=True,
                            container=True
                        )
                        submit = gr.Button("Send", variant="primary")
                        reset = gr.Button("Reset", variant="secondary")
                        
                with gr.Column(scale=1):
                    image_input = gr.Image(
                        label="Upload Image",
                        type="pil",
                        show_label=True,
                        container=True,
                        height=300,
                        sources=["upload", "clipboard"]
                    )
                    image_output = gr.Image(
                        label="Processed Image",
                        type="pil",
                        show_label=True,
                        container=True,
                        height=300
                    )
            
            # Set up event handlers
            submit.click(
                fn=self.process_interaction,
                inputs=[message, image_input, chatbot],
                outputs=[chatbot, image_output],
                api_name="process"
            ).then(
                fn=lambda: "",
                outputs=[message]
            )
            
            message.submit(
                fn=self.process_interaction,
                inputs=[message, image_input, chatbot],
                outputs=[chatbot, image_output],
                api_name="process_enter"
            ).then(
                fn=lambda: "",
                outputs=[message]
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
        server_port=7862,
        share=False,  # Disable sharing to avoid cross-origin issues
        show_error=True,
        allowed_paths=["test_images"],  # Allow access to test images
        quiet=True  # Reduce console output
    )

if __name__ == "__main__":
    main() 