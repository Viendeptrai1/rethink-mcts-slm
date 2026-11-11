import re

def is_palindrome(text: str) -> bool:
    # Remove non-alphanumeric characters and convert to lowercase
    cleaned_text = re.sub(r'[^A-Za-z0-9]', '', text).lower()
    # Check if the cleaned text is equal to its reverse
    return cleaned_text == cleaned_text[::-1]