from typing import List

def rolling_max(numbers: List[int]) -> List[int]:
    if not numbers:
        return []
    
    max_list = []
    current_max = numbers[0]
    
    for number in numbers:
        if number > current_max:
            current_max = number
        max_list.append(current_max)
    
    return max_list