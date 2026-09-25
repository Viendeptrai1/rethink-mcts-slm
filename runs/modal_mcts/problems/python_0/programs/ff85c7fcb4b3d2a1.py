from typing import List
import bisect

def has_close_elements(numbers: List[float], threshold: float) -> bool:
    # Step 1: Sort the list of numbers
    numbers.sort()
    
    # Step 2: Iterate through the sorted list and use binary search to find close elements
    for i in range(len(numbers)):
        # Find the left boundary of the range within the threshold
        left_bound = numbers[i] - threshold
        # Find the right boundary of the range within the threshold
        right_bound = numbers[i] + threshold
        
        # Use binary search to find the first element greater than or equal to left_bound
        left_index = bisect.bisect_left(numbers, left_bound)
        # Use binary search to find the first element greater than right_bound
        right_index = bisect.bisect_right(numbers, right_bound)
        
        # Check if there is any element in the range (left_index, right_index) that is not the current element
        for j in range(left_index, right_index):
            if j != i and abs(numbers[i] - numbers[j]) < threshold:
                return True
    
    return False