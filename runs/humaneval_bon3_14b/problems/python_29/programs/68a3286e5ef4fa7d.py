from typing import List


def filter_by_prefix(strings: List[str], prefix: str) -> List[str]:
    """Filter an input list of strings only for ones that start with a given prefix."""
    return [s for s in strings if s.startswith(prefix)]


# Test cases
if __name__ == "__main__":
    print(filter_by_prefix([], 'a'))  # Output: []
    print(filter_by_prefix(['abc', 'bcd', 'cde', 'array'], 'a'))  # Output: ['abc', 'array']