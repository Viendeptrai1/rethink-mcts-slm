def maximum(arr, k):
    """
    Given an array arr of integers and a positive integer k, return a sorted list 
    of length k with the maximum k numbers in arr.
    """
    if k == 0:
        return []
    
    # Use heapq.nlargest to get the k largest elements efficiently
    # Then sort them in ascending order as required by the output format
    import heapq
    top_k = heapq.nlargest(k, arr)
    return sorted(top_k)