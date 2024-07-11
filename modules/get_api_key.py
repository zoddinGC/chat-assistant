import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_API() -> str:
    return os.getenv('OPENAI_API_KEY')

if __name__ == '__main__':
    get_API()
