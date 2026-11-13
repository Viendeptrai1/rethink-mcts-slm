def sort_array(array):
    """
    Given an array of non-negative integers, return a copy of the given array after sorting,
    you will sort the given array in ascending order if the sum( first index value, last index value) is odd,
    or sort it in descending order if the sum( first index value, last index value) is even.

    Note:
    * don't change the given array.
    """
    # Return a copy immediately for empty list or single element
    if not array:
        return []
    if len(array) == 1:
        return [array[0]]

    # Get first and last values
    first_val = array[0]
    last_val = array[-1]

    # Calculate sum
    total = first_val + last_val

    # Sort based on parity of sum
    # Create a copy to avoid modifying the original array
    sorted_copy = array.copy()
    
    if total % 2 == 1:
        # Odd sum: sort ascending
        sorted_copy.sort()
    else:
        # Even sum: sort descending
        sorted_copy.sort(reverse=True)
    
    return sorted_copy