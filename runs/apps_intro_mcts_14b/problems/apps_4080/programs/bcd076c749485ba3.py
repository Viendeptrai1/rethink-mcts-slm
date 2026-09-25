import sys
from collections import defaultdict

def main():
    import sys
    import heapq
    
    def read_ints():
        return list(map(int, sys.stdin.readline().split()))
    
    n, m = read_ints()
    a = read_ints()
    
    segments = []
    for _ in range(m):
        l, r = read_ints()
        segments.append((l-1, r-1))
    
    # Initialize the difference array
    diff = [0] * (n + 1)
    
    # Apply the segments to the difference array
    for l, r in segments:
        diff[l] += 1
        diff[r + 1] -= 1
    
    # Compute the prefix sum to get the final array after applying segments
    current = 0
    max_val = float('-inf')
    min_val = float('inf')
    for i in range(n):
        current += diff[i]
        max_val = max(max_val, current + a[i])
        min_val = min(min_val, current + a[i])
    
    # Calculate the maximum difference
    max_diff = max_val - min_val
    
    # To find the actual segments that give this maximum difference
    # We need to recompute the prefix sum and track the segments
    current = 0
    max_val = float('-inf')
    min_val = float('inf')
    max_pos = None
    min_pos = None
    for i in range(n):
        current += diff[i]
        if current + a[i] == max_val:
            max_pos = i
        if current + a[i] == min_val:
            min_pos = i
    
    # Now we need to find the segments that contribute to the max and min positions
    selected_segments = set()
    for l, r in segments:
        if l <= max_pos <= r or l <= min_pos <= r:
            selected_segments.add((l, r))
    
    # Convert the selected segments back to their original indices
    selected_indices = []
    for i, (l, r) in enumerate(segments):
        if (l, r) in selected_segments:
            selected_indices.append(i + 1)
    
    # Output the result
    print(max_diff)
    print(len(selected_indices))
    print(*selected_indices)

if __name__ == "__main__":
    main()