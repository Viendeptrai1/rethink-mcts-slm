def maximum(arr, k):
    """
    Given an array arr of integers and a positive integer k, return a sorted list 
    of length k with the maximum k numbers in arr.
    """
    # Step 1: Sort the array in descending order
    sorted_arr = sorted(arr, reverse=True)
    
    # Step 2: Select the first k elements
    max_k_elements = sorted_arr[:k]
    
    # Step 3: Return the sorted list of the selected elements
    return sorted(max_k_elements)

# Example usage:
# print(maximum([-3, -4, 5], 3))  # Output: [-4, -3, 5]
# print(maximum([4, -4, 4], 2))   # Output: [4, 4]
# print(maximum([-3, 2, 1, 2, -1, -2, 1], 1))  # Output: [2]