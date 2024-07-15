# Python libraries
import numpy as np

from uuid import uuid4
from langchain.docstore.document import Document

# Local imports
from modules.tokenize_text import create_text_splitter

def embedding_in_chunks(data: dict) -> list[Document]:
    """
        This function receives a data in dictionary format with
        txt and type for key:value. Then, the function will split the
        text using tokenization with 500 tokens and add into chunks in
        a Document format for Langchain processing.

        :param data: A dictionary with all key:value for chunks
        :return: A list with Langchain's Document objects with page content
        (splitted text) and metadata with 'id' (uuid4 string), 'type' (str),
        and 'chunk' (int)
    """
    # Create chunks list to return
    chunks = []

    # Create a text splitter based on tokens size (chunks)
    text_splitter = create_text_splitter()

    # Split the text and append in chunk
    for txt, type in data.items():
        # Split text based on tokens
        texts = text_splitter.split_text(txt)

        chunks.extend([Document(
            page_content=texts[i],
            metadata={
                'id': str(uuid4()),
                'type': type,
                'chunk': i + len(chunks)
            }
        ) for i in range(len(texts))])

    return chunks

if __name__ == '__main__':
    embedding_in_chunks()
