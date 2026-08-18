def clean_string(input_string: str) -> str:
    """Removes unwanted characters from a string."""
    return ''.join(e for e in input_string if e.isalnum() or e.isspace())


def split_into_words(input_string: str) -> list:
    """Splits a string into individual words."""
    cleaned_string = clean_string(input_string)
    return cleaned_string.split() if cleaned_string else []


def calculate_word_frequency(words: list) -> dict:
    """Calculates frequency of each word in a list."""
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    return frequency


def print_word_frequency(frequency: dict) -> None:
    """Prints the word frequency in a readable format."""
    for word, count in frequency.items():
        print(f'{word}: {count}')