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
    
    # Create a dictionary to store the segments that affect each position
    pos_to_segments = defaultdict(list)
    for j, (l, r) in enumerate(segments):
        pos_to_segments[l-1].append(j)
        pos_to_segments[r].append(-j-1)
    
    # Initialize the array b with the same values as a
    b = a[:]
    
    # Priority queue to keep track of the minimum value in the current window
    min_heap = []
    
    # Iterate over each position in the array
    for i in range(n):
        # Add the segments that start at this position to the heap
        for j in pos_to_segments[i]:
            if j >= 0:
                heapq.heappush(min_heap, (b[i], j))
        
        # Remove the segments that end at this position from the heap
        while min_heap and min_heap[0][1] < 0 and -min_heap[0][1]-1 <= i:
            heapq.heappop(min_heap)
        
        # If the heap is not empty, decrease the value at this position
        if min_heap:
            b[i] -= 1
    
    # Calculate the maximum and minimum values in the modified array
    max_b = max(b)
    min_b = min(b)
    
    # Calculate the maximum possible value of max_b - min_b
    d = max_b - min_b
    
    # Find the subset of segments that achieves this maximum value
    used_segments = set()
    for i in range(n):
        for j in pos_to_segments[i]:
            if j >= 0 and b[i] == a[i] - 1:
                used_segments.add(j)
    
    # Prepare the output
    q = len(used_segments)
    c = list(used_segments)
    
    # Print the results
    print(d)
    print(q)
    print(*c)

if __name__ == "__main__":
    main()