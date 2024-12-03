import os
import openai
from openai.error import OpenAIError
import logging
from logging.handlers import RotatingFileHandler
import time
import re
import json

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Load the OpenAI API key from an environment variable
openai.api_key = os.environ.get('OPENAI_API_KEY')
if not openai.api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

def sanitize_input(text):
    # Implement input sanitization logic here
    # For example, remove HTML tags or escape special characters
    sanitized_text = re.sub('<[^<]+?>', '', text)
    return sanitized_text

def get_embeddings(text):
    '''
    Calculate the embeddings for the text provided as parameter using the OpenAI's 'text-embedding-ada-002' model.
    Then, return a list of the embeddings.
    
    :param text: The text to be embedded.
    :return: A list of embeddings or raises an exception if an error occurs.
    '''
    if not isinstance(text, str) or not text:
        raise ValueError("Input text must be a non-empty string.")
    
    sanitized_text = sanitize_input(text)
    
    try:
        # Call the OpenAI API to get the embeddings for the provided text
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=sanitized_text
        )
        # Extract the embeddings from the response
        embeddings = response['data'][0]['embedding']
        return embeddings
    except OpenAIError as e:
        # Log the error without exposing sensitive information
        logger.error(f"An OpenAIError occurred: {e.__class__.__name__}")
        raise
    except Exception as e:
        # Log the unexpected error without exposing sensitive information
        logger.error(f"An unexpected error occurred: {e.__class__.__name__}")
        raise

# Example usage:
# try:
#     embeddings = get_embeddings("This is a test text.")
#     print(embeddings)
# except Exception as e:
#     # Handle the exception, e.g., display a user-friendly message or take other appropriate actions
#     print("An error occurred while processing your request.")

