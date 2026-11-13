from typing import List

def rescale_to_unit(numbers: List[float]) -> List[float]:
    min_num = min(numbers)
    max_num = max(numbers)
    if max_num == min_num:
        return [0.0] * len(numbers)
    return [(x - min_num) / (max_num - min_num) for x in numbers]