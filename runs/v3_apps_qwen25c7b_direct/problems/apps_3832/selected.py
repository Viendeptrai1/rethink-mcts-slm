import sys
from typing import List

def min_hours_to_build_houses(hills: List[int]) -> List[int]:
    n = len(hills)
    max_k = (n + 1) // 2
    result = [0] * max_k
    
    for k in range(1, max_k + 1):
        current_min_hours = float('inf')
        for start in range(n - k + 1):
            current_hours = 0
            for i in range(start, start + k):
                current_hours += max(0, hills[i] - hills[start])
            current_min_hours = min(current_min_hours, current_hours)
        result[k-1] = current_min_hours
    
    return result

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
hills = list(map(int, data[1:]))

# Calculate and print results
results = min_hours_to_build_houses(hills)
print(" ".join(map(str, results)))