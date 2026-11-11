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
    
    # To find the segments that contribute to this maximum difference,
    # we need to track which segments were used.
    # We'll use a priority queue to keep track of the segments that contribute
    # to the maximum and minimum values.
    
    # Priority queues for max and min values
    max_heap = []
    min_heap = []
    
    # Track the segments that contribute to the max and min values
    max_segments = {}
    min_segments = {}
    
    for i in range(n):
        val = a[i] + diff[i]
        if val == max_val:
            heapq.heappush(max_heap, (-diff[i], i))
            max_segments[i] = []
        if val == min_val:
            heapq.heappush(min_heap, (diff[i], i))
            min_segments[i] = []
    
    # Trace back to find the segments that contributed to these values
    for i in range(n):
        if diff[i] != 0:
            if i in max_segments:
                for l, r in segments:
                    if l <= i + 1 <= r:
                        max_segments[i].append(l)
            if i in min_segments:
                for l, r in segments:
                    if l <= i + 1 <= r:
                        min_segments[i].append(l)
    
    # Now we need to find a subset of segments that maximizes the difference
    # We can use a greedy approach to select segments that contribute to the max and min values
    
    used_segments = set()
    for i in range(n):
        if i in max_segments:
            for seg in max_segments[i]:
                used_segments.add(seg)
        if i in min_segments:
            for seg in min_segments[i]:
                used_segments.add(seg)
    
    # Convert the set to a sorted list
    used_segments = sorted(list(used_segments))
    
    # Output the result
    print(d)
    print(len(used_segments))
    print(' '.join(map(str, used_segments)))

if __name__ == "__main__":
    main()