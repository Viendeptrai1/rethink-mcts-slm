from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:
    # Step 1: Sort the list of numbers
    numbers.sort()
    
    # Step 2: Iterate through the sorted list and check the difference between consecutive elements
    for i in range(len(numbers) - 1):
        if abs(numbers[i] - numbers[i + 1]) < threshold:
            return True
    
    # If no such pair is found, return False
    return False