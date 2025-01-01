import streamlit as st
import asyncio
import logging
from typing import List, Optional
from datetime import datetime
import uuid

from src.infrastructure.di.container import Container
from src.infrastructure.config.settings import Settings
from src.domain.entities import Document

# Configure logging to help track application behavior and debug issues
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StreamlitApp:
    """
    Main Streamlit application class that handles the UI and interaction logic.
    This class maintains clean architecture by delegating business logic to use cases.
    """
    def __init__(self):
        # Initialize container and settings
        self.container = Container()
        self.container.config()
        
        # Initialize use cases
        self.chat_completion = self.container.chat_completion()
        self.document_ingestion = self.container.document_ingestion()
        
        # Initialize session state if needed
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'session_id' not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())

    def setup_page(self):
        """Configure the Streamlit page layout and styling."""
        st.set_page_config(
            page_title="RAG Chatbot",
            page_icon="🤖",
            layout="wide"
        )
        
        st.title("RAG-Enabled Chatbot")
        
        # Add custom CSS for better chat message display
        st.markdown("""
        <style>
        .user-message {
            background-color: #e6f3ff;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
        }
        .assistant-message {
            background-color: #f0f0f0;
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
        }
        </style>
        """, unsafe_allow_html=True)

    def render_chat_messages(self):
        """Display chat messages with appropriate styling."""
        for message in st.session_state.messages:
            with st.container():
                if message["role"] == "user":
                    st.markdown(f"""
                    <div class="user-message">
                        <strong>You:</strong> {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="assistant-message">
                        <strong>Assistant:</strong> {message["content"]}
                    </div>
                    """, unsafe_allow_html=True)

    async def process_user_message(self, user_input: str):
        """
        Process user input and generate response using the chat completion use case.
        
        Args:
            user_input: The user's message text
        """
        try:
            # Add user message to state
            st.session_state.messages.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.utcnow()
            })
            
            # Generate response using chat completion use case
            response = await self.chat_completion.execute(
                session_id=st.session_state.session_id,
                user_input=user_input
            )
            
            # Add assistant response to state
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.content,
                "timestamp": response.timestamp
            })
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            st.error("An error occurred while processing your message. Please try again.")

    async def process_document_upload(self, uploaded_file):
        """
        Process uploaded document for RAG context.
        
        Args:
            uploaded_file: The uploaded file from Streamlit
        """
        try:
            # Read file content
            content = uploaded_file.read()
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            
            # Create document entity
            document = Document(
                content=content,
                source=uploaded_file.name,
                metadata={
                    "filename": uploaded_file.name,
                    "upload_time": datetime.utcnow().isoformat()
                }
            )
            
            # Use document ingestion use case
            await self.document_ingestion.execute(
                documents=[document],
                chunk_size=1000  # Configure based on your needs
            )
            
            st.success(f"Successfully processed document: {uploaded_file.name}")
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            st.error("An error occurred while processing the document. Please try again.")

    def render_sidebar(self):
        """Render the sidebar with document upload and configuration options."""
        with st.sidebar:
            st.header("Document Upload")
            uploaded_file = st.file_uploader(
                "Upload a document for context",
                type=['txt', 'pdf', 'docx']
            )
            
            if uploaded_file:
                if st.button("Process Document"):
                    asyncio.run(self.process_document_upload(uploaded_file))
            
            st.header("Configuration")
            st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Controls randomness in responses"
            )

    def render_chat_interface(self):
        """Render the main chat interface."""
        # Display chat messages
        self.render_chat_messages()
        
        # Chat input
        with st.container():
            user_input = st.text_input(
                "Your message",
                key="user_input",
                placeholder="Type your message here..."
            )
            
            if st.button("Send") or (user_input and user_input != st.session_state.get('last_input', '')):
                if user_input:
                    st.session_state.last_input = user_input
                    asyncio.run(self.process_user_message(user_input))
                    # Clear input after sending
                    st.experimental_rerun()

def main():
    """Main function to run the Streamlit application."""
    try:
        # Create and setup application
        app = StreamlitApp()
        app.setup_page()
        
        # Render sidebar and chat interface
        app.render_sidebar()
        app.render_chat_interface()
        
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error("An error occurred while starting the application. Please check the logs.")

if __name__ == "__main__":
    main()