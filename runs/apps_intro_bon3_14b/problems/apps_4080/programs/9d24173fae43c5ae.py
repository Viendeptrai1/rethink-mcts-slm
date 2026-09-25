import sys
from collections import defaultdict

def main():
    import sys
    import heapq
    
    def read_ints():
        return map(int, sys.stdin.readline().split())
    
    n, m = read_ints()
    a = list(read_ints())
    
    segments = []
    for _ in range(m):
        l, r = read_ints()
        segments.append((l, r))
    
    # Create a dictionary to store the segments that cover each index
    index_segments = defaultdict(list)
    for j, (l, r) in enumerate(segments):
        for i in range(l-1, r):
            index_segments[i].append(j)
    
    # Initialize the max heap and min heap
    max_heap = []
    min_heap = []
    
    # Initialize the result variables
    max_diff = 0
    selected_segments = []
    
    # Iterate over each index in the array
    for i in range(n):
        # Decrease the values in the max heap by 1
        while max_heap and max_heap[0][0] < a[i]:
            heapq.heappop(max_heap)
        
        # Decrease the values in the min heap by 1
        while min_heap and min_heap[0][0] < a[i]:
            heapq.heappop(min_heap)
        
        # Add the current value to both heaps
        heapq.heappush(max_heap, (a[i], i))
        heapq.heappush(min_heap, (a[i], i))
        
        # Calculate the current maximum and minimum values
        current_max = max_heap[0][0]
        current_min = min_heap[0][0]
        
        # Update the maximum difference
        if current_max - current_min > max_diff:
            max_diff = current_max - current_min
            selected_segments = index_segments[i]
    
    # Print the result
    print(max_diff)
    print(len(selected_segments))
    print(' '.join(map(str, [s + 1 for s in selected_segments])))

if __name__ == "__main__":
    main()