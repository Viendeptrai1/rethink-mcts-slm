def is_rotationally_symmetric(n, m, segments):
    def rotate_segment(segment, k):
        return ((segment[0] - 1 + k) % n + 1, (segment[1] - 1 + k) % n + 1)

    def rotate_segments(segments, k):
        return {rotate_segment(segment, k) for segment in segments}

    original_segments = set(segments)
    
    for k in range(1, n):
        rotated_segments = rotate_segments(original_segments, k)
        if rotated_segments == original_segments:
            return "Yes"
    
    return "No"

# Reading input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
segments = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(m)]

# Output the result
print(is_rotationally_symmetric(n, m, segments))