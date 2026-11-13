def sort_array(array):
    """
    Given an array of non-negative integers, return a copy of the given array after sorting,
    you will sort the given array in ascending order if the sum( first index value, last index value) is odd,
    or sort it in descending order if the sum( first index value, last index value) is even.

    Note:
    * don't change the given array.
    """
    if not array:
        return []
    
    if len(array) == 1:
        return array[:]
    
    first_value = array[0]
    last_value = array[-1]
    total_sum = first_value + last_value
    
    sorted_array = array[:]
    
    if total_sum % 2 == 1:
        sorted_array.sort()
    else:
        sorted_array.sort(reverse=True)
    
    return sorted_array