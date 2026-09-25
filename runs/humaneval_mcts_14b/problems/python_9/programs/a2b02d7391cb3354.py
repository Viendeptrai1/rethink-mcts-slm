from typing import List


def rolling_max(numbers: List[int]) -> List[int]:
    if not numbers:
        return []
    
    rolling_max_values = []
    current_max = numbers[0]
    
    for number in numbers:
        if number > current_max:
            current_max = number
        rolling_max_values.append(current_max)
    
    return rolling_max_values