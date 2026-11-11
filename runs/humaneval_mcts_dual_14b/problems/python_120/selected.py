def maximum(arr, k):
    """
    Given an array arr of integers and a positive integer k, return a sorted list 
    of length k with the maximum k numbers in arr.
    """
    # Sort the array in ascending order
    sorted_arr = sorted(arr)
    # Return the last k elements from the sorted array
    return sorted_arr[-k:]