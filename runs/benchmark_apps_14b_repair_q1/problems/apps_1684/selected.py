def is_rotationally_symmetric(n, m, segments):
    # Create a set of original segments
    original_segments = set(segments)
    
    # Function to rotate a segment by k units
    def rotate_segment(a, b, k):
        return ((a - 1 + k) % n + 1, (b - 1 + k) % n + 1)
    
    # Check for each k from 1 to n-1
    for k in range(1, n):
        rotated_segments = set()
        for a, b in segments:
            rotated_a, rotated_b = rotate_segment(a, b, k)
            # Ensure the segment is stored in the correct order
            if rotated_a > rotated_b:
                rotated_a, rotated_b = rotated_b, rotated_a
            rotated_segments.add((rotated_a, rotated_b))
        
        # If the rotated segments match the original, it's symmetric
        if rotated_segments == original_segments:
            return "Yes"
    
    return "No"

# Read input
n, m = map(int, input().split())
segments = [tuple(map(int, input().split())) for _ in range(m)]

# Output the result
print(is_rotationally_symmetric(n, m, segments))