from typing import List

def has_close_elements(numbers: List[float], threshold: float) -> bool:
    """ Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.
    """
    if len(numbers) < 2:
        return False
    
    # Sort the list to make it easier to find close elements
    numbers.sort()
    
    # Iterate through the sorted list and check adjacent elements
    for i in range(len(numbers) - 1):
        if abs(numbers[i] - numbers[i + 1]) < threshold:
            return True
    
    return False

# Test cases
print(has_close_elements([1.0, 2.0, 3.0], 0.5))  # False
print(has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3))  # True