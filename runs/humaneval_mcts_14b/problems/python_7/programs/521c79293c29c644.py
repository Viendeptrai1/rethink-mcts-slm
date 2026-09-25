from typing import List


def filter_by_substring(strings: List[str], substring: str) -> List[str]:
    """ 
    Filter an input list of strings only for ones that contain the given substring.
    
    If the substring is an empty string, all strings will be matched.
    
    >>> filter_by_substring([], 'a')
    []
    >>> filter_by_substring(['abc', 'bacd', 'cde', 'array'], 'a')
    ['abc', 'bacd', 'array']
    >>> filter_by_substring(['abc', 'bacd', 'cde', 'array'], '')
    ['abc', 'bacd', 'cde', 'array']
    """
    return [s for s in strings if substring in s]