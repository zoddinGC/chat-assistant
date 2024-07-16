# Python libraries
import os
from dotenv import load_dotenv

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


if __name__ == '__main__':
    get_API()
