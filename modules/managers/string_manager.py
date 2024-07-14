# Python libraries
import numpy as np

from re import findall, sub, compile, IGNORECASE
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_numbers(input_string: str) -> list[str]:
    # Find all sequences of digits in the string
    numbers = findall(r'\d+', input_string)
    return numbers

def transform_github_url(url: str) -> str:
    # Transform the GitHub URL to raw content URL
    if 'github.com' in url:
        return url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
    return url

def clean_text(pdf_text: str) -> str:
    # Remove line breaks
    cleaned_text = pdf_text.replace('\n', ' ')

    # Remove other non-human-readable indicators (like \x84 in your example)
    cleaned_text = sub(r'\\x[0-9A-Fa-f]{2}', '', cleaned_text)

    # Remove extra spaces
    cleaned_text = sub(r'\s+', ' ', cleaned_text).strip()

    return cleaned_text

def find_most_similar_substrings(text, substrings):
    """
    Find the most similar substrings within text.

    :param text: The main text to search within.
    :param substrings: List of substrings to match against the text.
    :return: The most similar substrings found in the text if their difference is lower than 0.15, otherwise the most similar one.
    """
    # Combine all text and substrings for vectorization
    combined_texts = [text] + substrings

    # Create TF-IDF Vectorizer and fit-transform the combined texts
    vectorizer = TfidfVectorizer().fit_transform(combined_texts)
    
    # Calculate the cosine similarity matrix
    cosine_similarities = cosine_similarity(vectorizer)

    # Extract the similarity scores for the main text against each substring
    similarity_scores = cosine_similarities[0][1:]

    # Find the indices of the two most similar substrings
    most_similar_indices = np.argsort(similarity_scores)[-2:][::-1]
    
    # Calculate the difference in similarity scores
    score_difference = similarity_scores[most_similar_indices[0]] - similarity_scores[most_similar_indices[1]]

    # Return the substrings based on the score difference
    if score_difference <= 0.15:
        return [most_similar_indices[1], most_similar_indices[0]]
    else:
        return [most_similar_indices[0]]

def find_best_match_positions(text, substrings):
    """
    Find the best matching substrings at the beginning and the end of the text.

    :param text: The main text to search within.
    :param substrings: List of substrings to match against the text.
    :return: The best matching substring for the beginning and the end of the text.
    """
    def get_best_match(text_segment, substrings):
        # Combine the segment and substrings for vectorization
        combined_texts = [text_segment] + substrings
        
        # Create TF-IDF Vectorizer and fit-transform the combined texts
        vectorizer = TfidfVectorizer().fit_transform(combined_texts)
        
        # Calculate the cosine similarity matrix
        cosine_similarities = cosine_similarity(vectorizer)
        
        # Extract the similarity scores for the segment against each substring
        similarity_scores = cosine_similarities[0][1:]
        
        # Find the index of the most similar substring
        most_similar_index = np.argmax(similarity_scores)
        
        # Return the most similar substring
        return most_similar_index

    # Consider a reasonable length for the beginning and end segments
    segment_length = 500  # Adjust based on your text size and requirements

    # Extract the beginning and end segments of the text
    beginning_segment = text[:segment_length]
    end_segment = text[-segment_length:]

    # Find the best matches for the beginning and end segments
    best_beginning_match = get_best_match(beginning_segment, substrings)
    best_end_match = get_best_match(end_segment, substrings)

    return best_beginning_match, best_end_match


if __name__ == '__main__':
    extract_numbers()
