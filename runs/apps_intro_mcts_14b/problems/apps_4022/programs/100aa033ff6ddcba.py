import sys
from typing import List, Tuple

def max_intersection_length(n: int, segments: List[Tuple[int, int]]) -> int:
    # Calculate the overall intersection of all segments
    left = min(segment[0] for segment in segments)
    right = max(segment[1] for segment in segments)
    
    # If the overall intersection is already empty, return 0
    if left > right:
        return 0
    
    # Calculate the intersection length if we remove each segment
    max_length = 0
    for i in range(n):
        # Remove the i-th segment
        new_left = max(segment[0] for j, segment in enumerate(segments) if i != j)
        new_right = min(segment[1] for j, segment in enumerate(segments) if i != j)
        
        # Calculate the intersection length of the remaining segments
        if new_left <= new_right:
            max_length = max(max_length, new_right - new_left + 1)
    
    return max_length

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    segments = []
    index = 1
    for _ in range(n):
        l = int(data[index])
        r = int(data[index + 1])
        segments.append((l, r))
        index += 2
    
    result = max_intersection_length(n, segments)
    print(result)

if __name__ == "__main__":
    main()