from streamlit.testing.v1 import AppTest
import pytest


def test_streamlit_chat_interface():
    """Test Streamlit UI components."""
    # Create a Streamlit test instance
    at = AppTest.from_file("src/main.py")
    at.run()

    # Test chat input
    assert at.text_input("Your message").exists()
    assert at.button("Send").exists()

    # Test document upload
    assert at.file_uploader("Upload a document for context").exists()
