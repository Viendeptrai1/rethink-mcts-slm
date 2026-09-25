from functools import reduce
from typing import List, Tuple

def sum_product(numbers: List[int]) -> Tuple[int, int]:
    if not numbers:
        return (0, 1)
    
    total_sum = sum(numbers)
    total_product = reduce(lambda x, y: x * y, numbers)
    
    return (total_sum, total_product)