from typing import List

def rescale_to_unit(numbers: List[float]) -> List[float]:
    min_num = min(numbers)
    max_num = max(numbers)
    if min_num == max_num:
        raise ValueError("All numbers in the list are the same. Cannot rescale.")
    return [(num - min_num) / (max_num - min_num) for num in numbers]