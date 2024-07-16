# Python libraries
import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

def get_API() -> str:
    """
        Get OpenAI API key from .env
    """
    return os.getenv('OPENAI_API_KEY')

def write_API(api_key: str):
    """
        Write the API key in .env

        :param api_key: The API KEY to write in .env
    """
    # Create and open the .env file in write mode
    with open('.env', 'w') as file:
        # Write the content to the file
        file.write(api_key)

def test_openai_api_key(api_key: str) -> tuple[bool, str]:
    """
        This function test if the given API key is valid on OpenAI

        :param api_key: A string representing the API key
    """
    openai.api_key = api_key

    try:
        # Make a simple API call to list available models
        response = openai.models.list()
        if response.data:
            return True, "API key is valid."
        else:
            return False, "API key is invalid or no models are available."
    except Exception as e:
        return False, f"An error occurred: {str(e)}"


if __name__ == '__main__':
    get_API()
