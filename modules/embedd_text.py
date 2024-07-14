import numpy as np

from transformers import AutoTokenizer, AutoModel
from uuid import uuid4

from langchain.docstore.document import Document

# Local imports
from modules.tokenize_text import create_text_splitter

def embedding_in_chunks(data: dict) -> tuple[list, np.array, tuple[int, int]]:
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
