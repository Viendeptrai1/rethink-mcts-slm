from typing import List, Optional

def longest(strings: List[str]) -> Optional[str]:
    if not strings:
        return None
    
    longest_string = strings[0]
    max_length = len(longest_string)
    
    for s in strings[1:]:
        if len(s) > max_length:
            longest_string = s
            max_length = len(s)
    
    return longest_string