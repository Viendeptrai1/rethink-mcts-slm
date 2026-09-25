import sys
from typing import List, Tuple

def max_intersection_length(n: int, segments: List[Tuple[int, int]]) -> int:
    # Sort segments by their left endpoint
    segments.sort()
    
    # Calculate the intersection of all segments
    left = segments[0][0]
    right = segments[0][1]
    for l, r in segments[1:]:
        left = max(left, l)
        right = min(right, r)
    
    # If the intersection of all segments is non-empty, return its length
    if left <= right:
        return right - left
    
    # Otherwise, we need to consider removing each segment one by one
    # and calculate the intersection of the remaining segments
    max_length = 0
    for i in range(n):
        # Calculate the intersection of all segments except the i-th one
        left = segments[0][0]
        right = segments[0][1]
        for j in range(1, n):
            if j != i:
                left = max(left, segments[j][0])
                right = min(right, segments[j][1])
        
        # Update the maximum length of the intersection
        if left <= right:
            max_length = max(max_length, right - left)
    
    return max_length

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    segments = []
    for i in range(n):
        l = int(data[2 * i + 1])
        r = int(data[2 * i + 2])
        segments.append((l, r))
    
    result = max_intersection_length(n, segments)
    print(result)

if __name__ == "__main__":
    main()