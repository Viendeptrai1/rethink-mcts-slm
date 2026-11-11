import sys
import heapq

def main():
    import sys
    import heapq
    
    def readints():
        return list(map(int, sys.stdin.readline().split()))
    
    n, m = readints()
    a = readints()
    segments = [readints() for _ in range(m)]
    
    # Initialize the difference array
    diff = [0] * (n + 1)
    
    # Apply the segments to the difference array
    for l, r in segments:
        diff[l - 1] += 1
        diff[r] -= 1
    
    # Compute the prefix sum to get the effect of all segments
    for i in range(1, n):
        diff[i] += diff[i - 1]
    
    # Find the maximum and minimum values after applying the segments
    max_val = max(a[i] + diff[i] for i in range(n))
    min_val = min(a[i] + diff[i] for i in range(n))
    
    # Calculate the maximum difference
    d = max_val - min_val
    
    # If d is 0, we don't need to apply any segments
    if d == 0:
        print(d)
        print(0)
        return
    
    # To find the segments that contribute to this maximum difference,
    # we need to track the segments that increase the maximum value
    # and decrease the minimum value.
    
    # We will use a priority queue to find the segments that contribute
    # to the maximum difference.
    
    # First, we need to find the segments that increase the maximum value
    max_heap = []
    for i, (l, r) in enumerate(segments):
        if a[l - 1] + diff[l - 1] < a[l - 1] + diff[l - 1] + 1:
            heapq.heappush(max_heap, (-1, i))
    
    # Then, we need to find the segments that decrease the minimum value
    min_heap = []
    for i, (l, r) in enumerate(segments):
        if a[r - 1] + diff[r - 1] > a[r - 1] + diff[r - 1] - 1:
            heapq.heappush(min_heap, (1, i))
    
    # Now, we need to find the segments that contribute to the maximum difference
    applied_segments = set()
    while max_heap and min_heap:
        max_diff, max_idx = heapq.heappop(max_heap)
        min_diff, min_idx = heapq.heappop(min_heap)
        
        if -max_diff > min_diff:
            applied_segments.add(max_idx)
        else:
            applied_segments.add(min_idx)
    
    # Print the result
    print(d)
    print(len(applied_segments))
    print(' '.join(map(str, [idx + 1 for idx in applied_segments])))

if __name__ == "__main__":
    main()