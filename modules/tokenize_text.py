import tiktoken

from langchain.text_splitter import RecursiveCharacterTextSplitter

def tiktoken_len(text):
    tokenizer = tiktoken.get_encoding('p50k_base')

    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )

    return len(tokens)

def create_text_splitter(chunk_size: int = 500) -> RecursiveCharacterTextSplitter:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=20,
        length_function=tiktoken_len,
        separators=['\n\n', '\n', ' ', '']
    )

    return text_splitter

if __name__ == '__main__':
    create_text_splitter()
