import openai
from html import escape

# Ensure that you have the OpenAI API key set in your environment variables
# or configure it here with openai.api_key = "your-api-key"

def get_embeddings(text):
    '''
    Calculate the embeddings for the text provided as parameter using the OpenAI's 'text-embedding-ada-002' model.
    Then, return a list of the embeddings.
    '''
    # Guideline #6: Validate the user input.
    # In this case, we ensure that the text is a string and not excessively long.
    if not isinstance(text, str) or len(text) > 1000:  # Adjust the length limit as needed
        raise ValueError("Input text must be a string with a maximum length of 1000 characters.")

    # Guideline #1: Escape the input before writing user input to the page.
    # This is not directly applicable as we are not writing to a web page, but if the embeddings
    # are to be displayed on a web page, the output should be escaped.
    # For demonstration, we'll escape the input text, although it's not necessary for the API call.
    safe_text = escape(text)

    # Call the OpenAI API to get the embeddings
    response = openai.Embedding.create(
        input=safe_text,
        model="text-embedding-ada-002"
    )

    # Extract the embeddings from the response
    embeddings = response['data'][0]['embedding']

    return embeddings

# Example usage:
# embeddings = get_embeddings("Example text to encode")
# print(embeddings)

