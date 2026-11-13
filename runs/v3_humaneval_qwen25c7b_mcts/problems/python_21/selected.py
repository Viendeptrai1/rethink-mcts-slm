from typing import List

def rescale_to_unit(numbers: List[float]) -> List[float]:
    if len(numbers) < 2:
        raise ValueError("List must contain at least two elements")
    
    min_val = min(numbers)
    max_val = max(numbers)
    range_val = max_val - min_val
    
    return [(x - min_val) / range_val for x in numbers]