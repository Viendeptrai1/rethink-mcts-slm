import sys
from math import atan2, pi

def read_vectors():
    n = int(sys.stdin.readline())
    vectors = []
    for _ in range(n):
        x, y = map(int, sys.stdin.readline().split())
        vectors.append((x, y))
    return vectors

def find_min_angle_pair(vectors):
    # Calculate polar angles and store them along with the index
    angles = [(atan2(y, x), i) for i, (x, y) in enumerate(vectors)]
    
    # Sort vectors by their polar angles
    angles.sort()
    
    min_angle = float('inf')
    min_pair = (-1, -1)
    
    # Compare adjacent pairs to find the minimum non-oriented angle
    for i in range(len(angles)):
        j = (i + 1) % len(angles)
        angle_diff = abs(angles[j][0] - angles[i][0])
        if angle_diff > pi:
            angle_diff = 2 * pi - angle_diff
        if angle_diff < min_angle:
            min_angle = angle_diff
            min_pair = (angles[i][1], angles[j][1])
    
    return min_pair

# Main execution
vectors = read_vectors()
result = find_min_angle_pair(vectors)
print(result[0] + 1, result[1] + 1)