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
    for j, (l, r) in enumerate(segments):
        for i in range(l-1, r):
            index_segments[i].append(j)
    
    # Initialize the priority queue with the minimum value in the array
    pq = []
    for i in range(n):
        heapq.heappush(pq, (-a[i], i))
    
    # Dictionary to keep track of the maximum value after applying segments
    max_values = {i: a[i] for i in range(n)}
    
    # Apply segments greedily
    applied_segments = set()
    while pq:
        current_max, idx = heapq.heappop(pq)
        current_max = -current_max
        
        # If the current maximum is already updated, skip
        if max_values[idx] != current_max:
            continue
        
        # Find the best segment to apply
        best_segment = None
        best_decrease = 0
        for j in index_segments[idx]:
            if j not in applied_segments:
                decrease = sum(1 for i in range(segments[j][0]-1, segments[j][1]) if max_values[i] == current_max)
                if decrease > best_decrease:
                    best_decrease = decrease
                    best_segment = j
        
        if best_segment is not None:
            applied_segments.add(best_segment)
            for i in range(segments[best_segment][0]-1, segments[best_segment][1]):
                max_values[i] -= 1
                heapq.heappush(pq, (-max_values[i], i))
    
    # Calculate the result
    result_max = max(max_values.values())
    result_min = min(max_values.values())
    result_diff = result_max - result_min
    
    # Prepare the output
    print(result_diff)
    print(len(applied_segments))
    print(' '.join(map(str, sorted(applied_segments) if applied_segments else [])))

if __name__ == "__main__":
    main()