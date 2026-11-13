import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    k = int(input_data[1])
    s = input_data[2]
    
    free_rooms = [i for i, char in enumerate(s) if char == '0']
    
    # We need to choose k+1 rooms from free_rooms.
    # Let the chosen indices be p_0, p_1, ..., p_k (sorted).
    # Farmer John will be at some p_i, and the max distance to any cow is max(p_k - p_i, p_i - p_0).
    # We want to minimize this value over all possible choices of k+1 rooms and all possible choices of FJ's room within that set.
    #
    # Observation:
    # If we fix the set of k+1 rooms, the optimal position for FJ is the median of these rooms to minimize the max distance.
    # Specifically, if we have rooms at indices x_0, x_1, ..., x_k, the best FJ position is x_{k//2} (or x_{(k+1)//2}, symmetric).
    # The cost would be max(x_k - x_{k//2}, x_{k//2} - x_0).
    #
    # However, we don't need to iterate over all subsets. Notice that if we pick a contiguous subarray of the sorted free_rooms list of length k+1,
    # say free_rooms[i : i+k+1], then the optimal FJ position within this set is the middle element.
    # Is it ever beneficial to pick a non-contiguous set of k+1 free rooms?
    # Suppose we pick a set S of k+1 indices. Let min_S = min(S) and max_S = max(S).
    # The cost is at least ceil((max_S - min_S) / 2) if we place FJ optimally in the middle? Not exactly.
    # Actually, if we fix min_S and max_S, and we have k-1 other points in between, the best we can do is place FJ such that the max distance is minimized.
    # But note: if we have a set of k+1 points, the minimal possible max distance from a center point to the extremes is determined by the span (max - min).
    # Specifically, if FJ is at x, cost = max(x - min, max - x). This is minimized when x = (min+max)/2, giving cost = (max-min)/2.
    # Since indices are integers, the cost is ceil((max-min)/2).
    # To minimize ceil((max-min)/2), we must minimize (max-min).
    # Therefore, we should pick k+1 free rooms such that the difference between the largest and smallest index is minimized.
    # This is achieved by picking a contiguous subarray of length k+1 from the sorted list of free rooms.
    #
    # So the algorithm is:
    # 1. Collect all indices of '0' into a list `free_rooms`.
    # 2. Iterate through all windows of length k+1 in `free_rooms`.
    # 3. For each window, calculate the span = last - first.
    # 4. The answer for this window is ceil(span / 2) = (span + 1) // 2.
    # 5. The global minimum is the answer.
    
    m = len(free_rooms)
    # We need k+1 rooms, so window size is k+1.
    window_size = k + 1
    
    min_max_dist = float('inf')
    
    # Iterate from i = 0 to m - window_size
    for i in range(m - window_size + 1):
        first = free_rooms[i]
        last = free_rooms[i + window_size - 1]
        span = last - first
        # The minimum max distance for this set is ceil(span / 2)
        current_dist = (span + 1) // 2
        if current_dist < min_max_dist:
            min_max_dist = current_dist
            
    print(min_max_dist)

if __name__ == "__main__":
    solve()