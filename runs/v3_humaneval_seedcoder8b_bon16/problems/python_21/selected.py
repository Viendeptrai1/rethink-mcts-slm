from typing import List

def rescale_to_unit(numbers: List[float]) -> List[float]:
    if len(numbers) < 2:
        return numbers  # Not enough elements to rescale
    
    min_val = min(numbers)
    max_val = max(numbers)
    range_val = max_val - min_val
    
    if range_val == 0:
        return [0.0] * len(numbers)  # All numbers are the same
    
    return [(x - min_val) / range_val for x in numbers]