# Python libraries
import tiktoken

# Local imports
from langchain.text_splitter import RecursiveCharacterTextSplitter

def tiktoken_len(text: str) -> int:
    """
        This function receives a text (string) and returns the size the 
        tokenized text.

        :param text: Any kind of string
        :return: A integer representing the size of the string in tokens
    """
    tokenizer = tiktoken.get_encoding('p50k_base')

    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )

    return len(tokens)

def create_text_splitter(chunk_size: int = 500) -> RecursiveCharacterTextSplitter:
    """
        This function creates a recursive text splitter based on the size of the 
        text in tokens.

        :param chunk_size: An integer representing the max size of the string 
        in tokens
        :return: A LangChain's RecursiveCharacterTextSplitter object
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=20,
        length_function=tiktoken_len,
        separators=['\n\n', '\n', ' ', '']
    )

    return text_splitter

if __name__ == '__main__':
    create_text_splitter()
