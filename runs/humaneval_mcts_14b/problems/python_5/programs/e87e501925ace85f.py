from typing import List

def intersperse(numbers: List[int], delimiter: int) -> List[int]:
    if not numbers:
        return []
    
    result = []
    for i in range(len(numbers) - 1):
        result.append(numbers[i])
        result.append(delimiter)
    result.append(numbers[-1])
    
    return result