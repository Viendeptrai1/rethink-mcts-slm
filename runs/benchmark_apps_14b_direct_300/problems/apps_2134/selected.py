import sys
from typing import List

def max_calm_group_sum(n: int, a: List[int], b: List[int]) -> int:
    # Sort students by their skill levels in descending order
    students = sorted(zip(a, b), key=lambda x: x[1], reverse=True)
    
    # Initialize the maximum sum to 0
    max_sum = 0
    
    # Iterate over all pairs of students
    for i in range(n):
        for j in range(i + 1, n):
            ai, bi = students[i]
            aj, bj = students[j]
            
            # Check if they can work together calmly
            if (ai & aj) == ai or (aj & ai) == aj:
                continue
            
            # Update the maximum sum
            max_sum = max(max_sum, bi + bj)
    
    return max_sum

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:n+1]))
b = list(map(int, data[n+1:2*n+1]))

# Output the result
print(max_calm_group_sum(n, a, b))