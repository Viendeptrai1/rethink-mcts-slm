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
    
    # Compute the prefix sums to get the effect of each segment
    for i in range(1, n):
        diff[i] += diff[i - 1]
    
    # Find the maximum and minimum values in the modified array
    max_val = max(a[i] + diff[i] for i in range(n))
    min_val = min(a[i] + diff[i] for i in range(n))
    
    # Calculate the maximum difference
    d = max_val - min_val
    
    # To find the segments that achieve this maximum difference, we need to
    # track which segments were used. We'll use a priority queue to help with this.
    
    # Create a priority queue to store the effect of each segment
    pq = []
    for i, (l, r) in enumerate(segments):
        heapq.heappush(pq, (-diff[l - 1], i + 1))
    
    # Track the segments used
    used_segments = []
    
    # Reconstruct the maximum difference using the priority queue
    current_max = max_val
    current_min = min_val
    while pq:
        effect, idx = heapq.heappop(pq)
        effect = -effect
        if current_max - current_min < d:
            break
        used_segments.append(idx)
        current_max -= effect
        current_min -= effect
    
    # Output the result
    print(d)
    print(len(used_segments))
    print(*used_segments)

if __name__ == "__main__":
    main()