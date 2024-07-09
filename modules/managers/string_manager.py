from re import findall, sub

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


if __name__ == '__main__':
    extract_numbers()
