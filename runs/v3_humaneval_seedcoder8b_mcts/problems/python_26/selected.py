from typing import List
from collections import Counter

def remove_duplicates(numbers: List[int]) -> List[int]:
    count = Counter(numbers)
    return [num for num in numbers if count[num] == 1]