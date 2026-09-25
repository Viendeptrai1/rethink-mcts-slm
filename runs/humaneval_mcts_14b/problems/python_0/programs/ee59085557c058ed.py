from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """ Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.
    """
    # Edge case: if the list is empty or contains only one element, return False
    if len(numbers) < 2:
        return False
    
    # Sort the list to make it easier to find close elements
    numbers.sort()
    
    # Iterate through the sorted list and check adjacent elements
    for i in range(len(numbers) - 1):
        if abs(numbers[i] - numbers[i + 1]) < threshold:
            return True
    
    # If no close elements are found, return False
    return False