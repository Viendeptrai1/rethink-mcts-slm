def is_rotationally_symmetrical(n, m, segments):
    def rotate_segment(segment, k):
        return ((segment[0] - 1 + k) % n + 1, (segment[1] - 1 + k) % n + 1)

    def sort_segments(segments):
        return sorted(sorted(segment) for segment in segments)

    original_segments = sort_segments(segments)
    
    for k in range(1, n):
        rotated_segments = sort_segments([rotate_segment(segment, k) for segment in segments])
        if rotated_segments == original_segments:
            return "Yes"
    
    return "No"

import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
segments = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(m)]

print(is_rotationally_symmetrical(n, m, segments))