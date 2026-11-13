from typing import *
from collections import *

def intersperse(numbers: List[int], delimiter: int) -> List[int]:
    if not numbers:
        return []
    
    result = []
    for i in range(len(numbers)):
        result.append(numbers[i])
        if i < len(numbers) - 1:
            result.append(delimiter)
    
    return result

# Test cases
print(intersperse([], 4))  # Output: []
print(intersperse([1, 2, 3], 4))  # Output: [1, 4, 2, 4, 3]