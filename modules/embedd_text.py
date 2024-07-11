import numpy as np

from transformers import AutoTokenizer, AutoModel
from uuid import uuid4

# Local imports
from modules.tokenize_text import create_text_splitter

def embed_text(text: str) -> str:
    # String for model AI in hugginface.co/models
    model_id = 'mrm8488/bert-base-portuguese-cased-finetuned-squad-v1-pt'

    # Load pre-trained model and tokenizer
    embedder = AutoTokenizer.from_pretrained(model_id)
    model = AutoModel.from_pretrained(model_id)

    # Encode text
    inputs = embedder(text, return_tensors="pt")
    outputs = model(**inputs)

    # Extract embeddings
    return outputs.last_hidden_state[0].detach().numpy()

def pad_embedding(embedding: np.array, pad_dimensions: tuple[int, int]):
    max_length, max_dim = pad_dimensions

    if embedding.shape[0] > max_length:
        embedding = embedding[:max_length]

    padded_embedding = np.pad(embedding, ((0, max_length - embedding.shape[0]), (0, max_dim - embedding.shape[1])), 'constant')

    return padded_embedding.flatten()

def embedding_in_chunks(data: dict) -> tuple[list, np.array, tuple[int, int]]:
    # Create chunks list to return
    chunks = []

    # Create a text splitter based on tokens size (chunks)
    text_splitter = create_text_splitter()

    # Split the text and append in chunk
    for txt, type in data.items():
        texts = text_splitter.split_text(txt)
        chunks.extend([{
            'id': str(uuid4()),
            'text': texts[i],
            'embedding': embed_text(texts[i]),
            'type': type,
            'chunk': i + len(chunks)
        } for i in range(len(texts))])

    # Find the max length and max embedding dimension
    max_length = max(item['embedding'].shape[0] for item in chunks)
    max_dim = max(item['embedding'].shape[1] for item in chunks)
    pad_dimensions = (max_length, max_dim)

    # Now retrieve the embed data for Faiss indexing method
    new_data = []
    for i, chunk in enumerate(chunks):
        # Get padded embed chunk
        pad_chunk = pad_embedding(chunk['embedding'], pad_dimensions)

        new_data.append(pad_chunk)
        chunks[i]['embedding'] = pad_chunk

    return (chunks, np.array(new_data), pad_dimensions)

if __name__ == '__main__':
    embedding_in_chunks()
