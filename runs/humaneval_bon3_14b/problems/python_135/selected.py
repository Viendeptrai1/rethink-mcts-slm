def can_arrange(arr):
    """Create a function which returns the largest index of an element which
    is not greater than or equal to the element immediately preceding it. If
    no such element exists then return -1. The given array will not contain
    duplicate values.

    Examples:
    can_arrange([1,2,4,3,5]) = 3
    can_arrange([1,2,3]) = -1
    """
    # Initialize the result as -1, assuming no such element is found
    result = -1
    
    # Iterate through the array starting from the second element
    for i in range(1, len(arr)):
        # Check if the current element is less than the previous element
        if arr[i] < arr[i - 1]:
            # Update the result with the current index
            result = i
    
    return result

# Test cases
print(can_arrange([1, 2, 4, 3, 5]))  # Output: 3
print(can_arrange([1, 2, 3]))        # Output: -1