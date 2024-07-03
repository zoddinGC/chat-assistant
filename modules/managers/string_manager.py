from re import findall

def extract_numbers(input_string: str) -> list[str]:
    # Find all sequences of digits in the string
    numbers = findall(r'\d+', input_string)
    return numbers


if __name__ == '__main__':
    extract_numbers()
