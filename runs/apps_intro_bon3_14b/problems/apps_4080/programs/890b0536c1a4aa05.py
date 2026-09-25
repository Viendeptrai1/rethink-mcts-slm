import sys
from collections import defaultdict

def main():
    import sys
    import heapq
    
    def read_ints():
        return list(map(int, sys.stdin.readline().split()))
    
    n, m = read_ints()
    a = read_ints()
    segments = [read_ints() for _ in range(m)]
    
    # Create a dictionary to store the segments that cover each index
    index_segments = defaultdict(list)
    for i, (l, r) in enumerate(segments):
        index_segments[l-1].append(i)
        index_segments[r].append(-i-1)
    
    # Initialize the array b with the same values as a
    b = a[:]
    
    # Priority queue to keep track of the minimum value in the current range
    min_heap = []
    max_value = float('-inf')
    min_value = float('inf')
    
    # Iterate through the array and apply the segments
    for i in range(n):
        # Add the segments that start at the current index
        for seg_index in index_segments[i]:
            if seg_index >= 0:
                heapq.heappush(min_heap, (a[i], seg_index))
        
        # Remove the segments that end at the current index
        while min_heap and min_heap[0][1] < 0 and -min_heap[0][1]-1 <= i:
            heapq.heappop(min_heap)
        
        # If there are segments applied, update the current value
        if min_heap:
            current_value = min_heap[0][0]
            b[i] = current_value
        
        # Update the maximum and minimum values
        max_value = max(max_value, b[i])
        min_value = min(min_value, b[i])
    
    # Calculate the result
    result = max_value - min_value
    
    # Find the segments that were applied
    applied_segments = set()
    for i in range(n):
        for seg_index in index_segments[i]:
            if seg_index >= 0 and b[i] == a[i]:
                applied_segments.add(seg_index)
    
    # Prepare the output
    print(result)
    print(len(applied_segments))
    print(' '.join(map(str, sorted(applied_segments) + 1)))

if __name__ == "__main__":
    main()