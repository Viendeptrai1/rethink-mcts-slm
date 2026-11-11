from typing import List

def rescale_to_unit(numbers: List[float]) -> List[float]:
    min_val = min(numbers)
    max_val = max(numbers)
    if min_val == max_val:
        raise ValueError("All numbers in the list are the same. Cannot rescale.")
    return [(x - min_val) / (max_val - min_val) for x in numbers]