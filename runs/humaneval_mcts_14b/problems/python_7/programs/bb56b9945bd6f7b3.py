from typing import List

def filter_by_substring(strings: List[str], substring: str) -> List[str]:
    """ Filter an input list of strings only for ones that contain given substring """
    return [s for s in strings if substring in s]

# Example usage
if __name__ == "__main__":
    print(filter_by_substring([], 'a'))  # Output: []
    print(filter_by_substring(['abc', 'bacd', 'cde', 'array'], 'a'))  # Output: ['abc', 'bacd', 'array']