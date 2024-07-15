# Python libraries
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.retrieval_qa.base import RetrievalQA
from uuid import uuid4

# Local imports
from modules.embedd_text import embedding_in_chunks
from modules.managers.folder_manager import check_folder_existence
from modules.managers.string_manager import find_most_similar_substrings, find_best_match_positions

def convert_seconds_to_minute(seconds:float) -> tuple[int, int]:
    """
        This function converts seconds (float like 123.66) to minutes 
        and remaining seconds (2 minutes, 3 seconds)
    """
    minutes = seconds // 60
    remaining_seconds = seconds % 60

    return int(minutes), int(remaining_seconds)

class IndexingData():
    def __init__(self, path: str or None=None) -> None:
        """
            This class is designed to create a library from a provided data. The data needs
            to be in Document format and splitted in chunks. After indexing the data, you can
            call a class method to retrieve a response from ChatGPT using Lanchain's OpenAI module.

            It is necessary to input your OPEN API KEY in a .env file with the name 'OPENAI_API_KEY'.

            :param path: If given, it will try to load a saved library locally. If not given, it will
            create just in the `create_library` method.
        """
        # Check if a path was provided. If yes, it will load a pre-saved context
        if path:
            self.__library = self.__load_local(path)
            self.__QA = self.__create_QA()

    def create_library(self, data: dict):
        """
            This method receives a data in dictionary with a format where `'key'=raw` text string and
            `'value'='type'` (in string like "text"). It will process in smalled chunks with 500 tokens
            each and create a Langchain Document object.

            It will create the `__library` and `__QA` instances to get a response from OpenAI's ChatGPT

            :param data: A dictionary with raw data and its type
        """
        # Get data um Document format
        docs = embedding_in_chunks(data=data)

        # Create the library and retriever with context
        self.__library = FAISS.from_documents(docs, OpenAIEmbeddings())
        self.__QA = self.__create_QA()

    def search_index(self, query: str, top_k: int = 5) -> dict:
        """
            This method receives a string query (text) as a question that needs to be answered. After
            that, it will try to find the best K matches (top_k) to the question provided based on the
            given data (library).

            :param query: A string text
            :param top_k: A integer representing how many similar items will be retrieved in the library
            :return: A dictionary with the most similar content
        """
        # Query the index
        answer = self.__library.similarity_search(query, k=top_k)  # Search for the 5 nearest neighbors

        return answer
    
    def __create_retriever(self) -> FAISS:
        """
            This method retrieve a Langchain's ChatGPT OpenAI object based on the indexed library (content).

            :return: FAISS object to retrieve ChatGPT response
        """
        # Retrieve information for library
        retriever = self.__library.as_retriever(
            search_type="mmr",
            search_kwargs={'k': 5}, # How many context will be retrieved
        )

        return retriever

    def __create_QA(self) -> RetrievalQA:
        """
            This method create a Question&Answer (QA) bot based on OpenAI ChatGPT. Questions without a
            good context will be answer as "I don't know" or something similar to it.

            :return: RetrievalQA
        """
        # Create a library retriever object
        retriever = self.__create_retriever()

        # Create a Question&Answer object to get ChatGPT response
        qa = RetrievalQA.from_chain_type(
            llm=OpenAI(),
            chain_type='stuff',
            retriever=retriever,
            return_source_documents=True
        )

        return qa
    
    def retrieve_from_GPT(self, query: str, threshold: float) -> tuple[dict, bool]: 
        """
            This method receives a query (question for ChatGPT) and return an answer based on the
            provided context to library. To avoid hallucination, first of all the method search for
            the best 3 context in library and, if not found any good context (p>threshold), it return
            a response of "I don't know".

            :param query: A string that will be provided to ChatGPT
            :param threshold: A flod representing the minimum confidence of the context found (close to 0 = best)
        """
        # Retrieve documents
        retrieved_docs = self.__library.similarity_search_with_score(query, k=3)

        # Implementing confidence threshold logic
        confident_docs = [doc[1] for doc in retrieved_docs if doc[1] < threshold]

        if not confident_docs:
            return (
                {
                    'query': query,
                    'run_name': str(uuid4),
                    'result': "Não sei. Sua pergunta está fora do escopo da aula.",
                    'source_documents': None
                },
                False
            )

        return (
            self.__QA.invoke({
                'query': query,
                'run_name': str(uuid4()),
                'language': 'portuguese',
            }), 
            True
        )
    
    def retrieve_context(self, query: str, raw_data: dict, threshold: float=0.3) -> dict:
        """
            This method will get the response from ChatGPT based on a user query and the context
            provided to library. It needs the user query, and raw data to find where the context exists
            so user can check the reference. The threshold argument is optional and closing it to zero
            means that the model will search for only the best context. Higher values mean a more random
            context.

            :param query: A string that will be provided to ChatGPT
            :param raw_data: A dictionary with the raw data, its type and other important metadata to reference
            :param threshold: A float representing the confidence score of the search context
        """
        # Get answer from ChatGPT
        answer, source_documents = self.retrieve_from_GPT(query, threshold)

        # Initialize the string that will be returned
        response = ''

        # Check if the answer is outside the knowledge
        if not source_documents:
            response  = f'Não há documento de apoio para esta pergunta, pois ela foge do escopo da aula.'
            return {
                'query': query,
                'response': response,
            }

        # Get context from answer
        doc_type, doc_text = answer['source_documents'][0].metadata['type'], answer['source_documents'][0].page_content

        # Try to find where the context has been provided
        if doc_type == 'text':
            response = 'O documento de apoio pode ser encontrado no arquivo de texto.'

        elif doc_type == 'pdf':
            pdf_content = raw_data['pdf']

            page = find_most_similar_substrings(doc_text, pdf_content['pages_text'])
            if len(page) > 1:
                response = f'O documento de apoio encontra-se entre as páginas {page[0]} e {page[1]} do PDF'
            else:
                response  = f'O documento de apoio encontra-se na a página {page[0]} do PDF'

        elif doc_type == 'video':
            segments = raw_data['video']
            times = find_best_match_positions(doc_text, segments[0])
            start_m, start_s = convert_seconds_to_minute(float(segments[1][times[0]][0]))
            end_m, end_s   = convert_seconds_to_minute(float(segments[1][times[0]][1]))
            response = f'O documento de apoio está no vídeo entre os minutos {start_m}:{start_s}-{end_m}:{end_s}'

        # Create a good response based on the provided ChatGPT's response + where the context was found
        response = answer['result'] + '\n' + response

        return {
            'query': query,
            'response': response,
        }

    def save_local(self, path: str):
        """
            This method will save the loaded library to a local file and it can be loaded later without
            pre-processing the raw data again.

            :param path: A string representing where the local file will be saved
        """
        max_char = path.rfind('/')
        if max_char <= 0: max_char = len(path)

        check_folder_existence(path[:max_char])
        
        self.__library.save_local(path)

    def __load_local(self, path: str) -> FAISS:
        """
            This method will load a saved library.

            :param path: A string representing where the local library is saved
        """
        return FAISS.load_local(
            path,
            OpenAIEmbeddings(),
            allow_dangerous_deserialization=True
        )
       
    @property
    def get_library(self) -> FAISS:
        return self.__library
    
    @property
    def get_QA(self) -> RetrievalQA:
        return self.__QA


if __name__ == '__main__':
    IndexingData()
