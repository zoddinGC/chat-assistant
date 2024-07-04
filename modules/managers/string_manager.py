from re import findall

def extract_numbers(input_string: str) -> list[str]:
    # Find all sequences of digits in the string
    numbers = findall(r'\d+', input_string)
    return numbers

def transform_github_url(url: str) -> str:
    if not 'raw' in url:
        url = url.replace('github', 'raw.githubusercontent')
        url = url.replace('/blob', '')

    return url


if __name__ == '__main__':
    extract_numbers()
