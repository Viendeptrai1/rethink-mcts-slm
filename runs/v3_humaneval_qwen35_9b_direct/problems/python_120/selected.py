def maximum(arr, k):
    if k == 0:
        return []
    if k == len(arr):
        return sorted(arr)
    
    # Use a min-heap of size k to keep track of the k largest elements
    import heapq
    min_heap = arr[:k]
    heapq.heapify(min_heap)
    
    for i in range(k, len(arr)):
        if arr[i] > min_heap[0]:
            heapq.heapreplace(min_heap, arr[i])
    
    # Sort the result in ascending order
    return sorted(min_heap)