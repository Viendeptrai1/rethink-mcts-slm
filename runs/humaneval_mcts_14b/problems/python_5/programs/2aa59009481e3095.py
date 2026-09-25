from typing import List

def intersperse(numbers: List[int], delimiter: int) -> List[int]:
    if len(numbers) <= 1:
        return numbers
    
    result = []
    for i in range(len(numbers) - 1):
        result.append(numbers[i])
        result.append(delimiter)
    result.append(numbers[-1])
    
    return result