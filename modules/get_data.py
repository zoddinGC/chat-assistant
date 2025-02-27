# Python libraries
import requests
import fitz
import io

# Local imports
from modules.managers.folder_manager import check_folder_existence
from modules.managers.string_manager import transform_github_url


def get_text_from_github(url: str) -> dict:
    """
        Receives a raw URL from github and get its content if it is a
        unique file. Example: a text.txt file will return a dictionary
        with the content and its type (text).

        :param url: A string for GitHub content
        :return: A dictionary with its content and type 'text':text content,
        'type':'text'
    """
    # Adjusted URL to fetch the raw content
    url = transform_github_url(url)

    # Make a GET request to fetch the raw file content
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Retrieve the content of the file
        file_content = response.text

        return {'text': file_content, 'type': 'text'}
    
    raise ValueError(f"Failed to retrieve data from {url!r}. Status code: {response.status_code}")

def get_pdf_from_github(url: str) -> dict:
    """
        Receives a raw URL from github and get its content if it is a
        unique file. Example: a document.pdf file will return a dictionary
        with the content and its type (PDF).

        :param url: A string for GitHub content
        :return: A dictionary with its content and type 'text':all text joined,
        'pages_text':a list with all content, each index indicates one page,
        'type':'pdf'
    """
    # Adjusted URL to fetch the raw content
    url = transform_github_url(url)

    # Make a GET request to fetch the raw PDF content
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Use io.BytesIO to handle the PDF content in memory
        pdf_file = io.BytesIO(response.content)
        
        # Open the PDF file using PyMuPDF
        pdf_document = fitz.open(stream=pdf_file, filetype="pdf")
        
        # Extract text from each page
        pdf_text = []
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            pdf_text.append(page.get_text())
        
        # Close the PDF document
        pdf_document.close()

        return {'text': ''.join(pdf_text), 'pages_text': pdf_text, 'type': 'pdf'}

    raise ValueError(f"Failed to retrieve data from {url!r}. Status code: {response.status_code}")

def save_video_from_github(url: str, save_path: str):
    """
        Retreive a video from a Github URL and save it as a local file. It is
        necessary to save to process instead of saving it in memory.

        :param url: A Github URL to the video
        :param save_path: A string containing the local to save the file
    """
    # Adjusted URL to fetch the raw content
    url = transform_github_url(url)

    # Make a GET request to fetch the raw video content
    response = requests.get(url, stream=True)

    # Check folder to save video
    check_folder_existence(save_path[:save_path.rfind('/')])

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Save the video content to a local file
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)

if __name__ == '__main__':
    pass