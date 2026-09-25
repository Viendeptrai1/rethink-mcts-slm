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
    
    # Sort segments by their right endpoint
    segments.sort(key=lambda x: x[1])
    
    # Initialize the difference array
    diff = [0] * (n + 1)
    
    # Apply the segments to the difference array
    for l, r in segments:
        diff[l - 1] += 1
        diff[r] -= 1
    
    # Compute the prefix sum to get the effect of segments on each position
    for i in range(1, n):
        diff[i] += diff[i - 1]
    
    # Compute the new array b
    b = [a[i] - diff[i] for i in range(n)]
    
    # Find the maximum and minimum values in b
    max_b = max(b)
    min_b = min(b)
    
    # Calculate the maximum possible value of max(b) - min(b)
    result = max_b - min_b
    
    # To find the segments that achieve this result, we need to backtrack
    # We will use a priority queue to keep track of the segments that contribute to the maximum value
    pq = []
    for i, (l, r) in enumerate(segments):
        heapq.heappush(pq, (-diff[l - 1], i))
    
    selected_segments = []
    while pq:
        val, idx = heapq.heappop(pq)
        if -val > 0:
            selected_segments.append(idx + 1)
    
    # Output the result
    print(result)
    print(len(selected_segments))
    print(*selected_segments)

if __name__ == "__main__":
    main()