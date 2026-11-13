def sort_array(array):
    """
    Given an array of non-negative integers, return a copy of the given array after sorting,
    you will sort the given array in ascending order if the sum( first index value, last index value) is odd,
    or sort it in descending order if the sum( first index value, last index value) is even.

    Note:
    * don't change the given array.
    """
    # Create a copy to avoid modifying the original array
    result = array.copy()
    
    # Handle edge cases: empty array or single element
    if len(result) <= 1:
        return result
    
    # Get first and last values
    first_value = result[0]
    last_value = result[-1]
    
    # Calculate sum and check parity
    total_sum = first_value + last_value
    
    # Sort based on parity: odd -> ascending (reverse=False), even -> descending (reverse=True)
    result.sort(reverse=(total_sum % 2 == 0))
    
    return result