from math import atan2, pi
from typing import List

def find_min_angle_pair(vectors: List[List[int]]) -> List[int]:
    angles = [(atan2(y, x), i) for i, (x, y) in enumerate(vectors)]
    sorted_angles = sorted(angles)
    
    min_angle = float('inf')
    result_pair = None
    
    for i in range(len(sorted_angles)):
        for j in range(i + 1, len(sorted_angles)):
            angle_diff = abs(sorted_angles[j][0] - sorted_angles[i][0])
            if angle_diff > pi:
                angle_diff = 2 * pi - angle_diff
            if angle_diff < min_angle:
                min_angle = angle_diff
                result_pair = (sorted_angles[i][1], sorted_angles[j][1])
    
    return result_pair[0] + 1, result_pair[1] + 1

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
vectors = [[int(data[2*i+1]), int(data[2*i+2])] for i in range(n)]

# Find and print the result
result = find_min_angle_pair(vectors)
print(result[0], result[1])