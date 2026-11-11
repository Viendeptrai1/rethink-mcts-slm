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
    
    # Initialize the difference array
    diff = [0] * (n + 1)
    
    # Apply the segments to the difference array
    for l, r in segments:
        diff[l - 1] += 1
        diff[r] -= 1
    
    # Compute the prefix sum to get the actual changes
    for i in range(1, n):
        diff[i] += diff[i - 1]
    
    # Find the maximum and minimum values in the modified array
    max_val = max(a[i] + diff[i] for i in range(n))
    min_val = min(a[i] + diff[i] for i in range(n))
    
    # Calculate the maximum difference
    max_diff = max_val - min_val
    
    # If the maximum difference is 0, we don't need any segments
    if max_diff == 0:
        print(0)
        print(0)
        return
    
    # To find the segments that contribute to this maximum difference,
    # we need to track which segments were used to achieve this.
    # We'll use a priority queue to keep track of the segments that
    # contribute to the maximum and minimum values.
    
    # Priority queues for max and min values
    max_heap = []
    min_heap = []
    
    # Track the segments that contribute to the max and min values
    max_segments = defaultdict(list)
    min_segments = defaultdict(list)
    
    for i in range(n):
        val = a[i] + diff[i]
        if val == max_val:
            max_segments[val].append(i + 1)
        if val == min_val:
            min_segments[val].append(i + 1)
    
    # Now, we need to find the segments that contribute to these max and min values
    # We'll use a greedy approach to select the segments that maximize the difference
    
    selected_segments = []
    
    # Add segments that contribute to the max value
    for val in sorted(max_segments.keys(), reverse=True):
        for seg in max_segments[val]:
            selected_segments.append(seg)
    
    # Add segments that contribute to the min value
    for val in sorted(min_segments.keys()):
        for seg in min_segments[val]:
            selected_segments.append(seg)
    
    # Remove duplicates and ensure we only select valid segments
    selected_segments = list(set(selected_segments))
    
    # Print the result
    print(max_diff)
    print(len(selected_segments))
    print(*selected_segments)

if __name__ == "__main__":
    main()