import numpy as np
import faiss

from tqdm.auto import tqdm

from modules.embedd_text import embedding_in_chunks, pad_embedding, embed_text

class IndexingData():
    def __init__(self, data: dict) -> None:
        self.__chunks, self.__data, self.__pad_dimensions = embedding_in_chunks(data=data)

        self.__index = self.__create_index()

    def __create_index(self) -> faiss.IndexFlatL2:
        # Get the embed data
        data = self.get_data

        # Get the dimensions to use in index
        dim = data[0].shape[0]

        # Create an index
        index = faiss.IndexFlatL2(dim)  # L2 distance (Euclidean)

        # Add data to the index
        index.add(data)

        return index
    
    def query_to_vector(self, query: str) -> np.array:
        embed_query = embed_text(query)
        padded_embed = pad_embedding(embed_query, pad_dimensions=self.get_pad_dimensions)

        return np.array(padded_embed).reshape(1, -1).astype('float32')

    def search_index(self, query: str, top_k: int = 5) -> tuple[int, int]:
        # Vectorize the query
        query_vector = self.query_to_vector(query)

        print(query_vector)

        # Query the index
        D, I = self.__index.search(query_vector, k=top_k)  # Search for the 5 nearest neighbors

        return D[0], I[0]
    
    @property
    def get_data(self) -> np.array:
        return self.__data
    
    @property
    def get_chunks(self) -> dict:
        return self.__chunks
    
    @property
    def get_pad_dimensions(self) -> tuple[int, int]:
        return self.__pad_dimensions


if __name__ == '__main__':
    IndexingData()
