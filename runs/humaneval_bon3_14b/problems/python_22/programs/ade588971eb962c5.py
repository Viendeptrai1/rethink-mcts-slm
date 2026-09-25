from typing import List, Any


def filter_integers(values: List[Any]) -> List[int]:
    """Filter given list of any python values only for integers."""
    return [value for value in values if isinstance(value, int)]


# Example usage
if __name__ == "__main__":
    print(filter_integers(['a', 3.14, 5]))  # Output: [5]
    print(filter_integers([1, 2, 3, 'abc', {}, []]))  # Output: [1, 2, 3]