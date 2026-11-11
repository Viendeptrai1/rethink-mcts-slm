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
    
    # Compute the prefix sum to get the effect of each segment
    for i in range(1, n):
        diff[i] += diff[i - 1]
    
    # Find the maximum and minimum values in the modified array
    max_val = max(a[i] + diff[i] for i in range(n))
    min_val = min(a[i] + diff[i] for i in range(n))
    
    # Calculate the maximum difference
    d = max_val - min_val
    
    # To find the segments that contribute to this maximum difference,
    # we need to track which segments were used.
    # We'll use a priority queue to keep track of the segments that increase the max or decrease the min.
    
    # Priority queues for max and min
    max_heap = []
    min_heap = []
    
    for i, (l, r) in enumerate(segments):
        # Calculate the effect of the segment
        effect = max(a[l - 1:r]) - min(a[l - 1:r])
        # Push the negative effect to max heap and positive effect to min heap
        heapq.heappush(max_heap, (-effect, i + 1))
        heapq.heappush(min_heap, (effect, i + 1))
    
    # Track the segments used
    used_segments = set()
    
    # Try to maximize the difference by using segments
    while max_heap and min_heap:
        # Get the segment that increases the max the most
        max_effect, max_index = heapq.heappop(max_heap)
        # Get the segment that decreases the min the most
        min_effect, min_index = heapq.heappop(min_heap)
        
        # If the segment is already used, skip it
        if max_index in used_segments or min_index in used_segments:
            continue
        
        # Use the segment
        used_segments.add(max_index)
        used_segments.add(min_index)
        
        # Recalculate the max and min values
        max_val = max(a[i] + diff[i] for i in range(n))
        min_val = min(a[i] + diff[i] for i in range(n))
        
        # Update the difference
        d = max_val - min_val
        
        # If the difference is maximized, break
        if d == max_val - min_val:
            break
    
    # Output the result
    print(d)
    print(len(used_segments))
    print(*used_segments)

if __name__ == "__main__":
    main()