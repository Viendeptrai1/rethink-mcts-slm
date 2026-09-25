import sys
from sortedcontainers import SortedList

def count_median_pairs(n, m, p):
    # Initialize a sorted list to keep track of the positions of elements
    positions = SortedList()
    # Dictionary to store the frequency of elements less than m
    less_count = {}
    # Dictionary to store the frequency of elements greater than m
    greater_count = {}
    
    # Iterate through the permutation
    for i in range(n):
        if p[i] < m:
            less_count[i] = len(positions)
            positions.add(i)
        elif p[i] > m:
            greater_count[i] = len(positions)
            positions.add(i)
    
    # Calculate the number of valid subarrays
    result = 0
    for i in range(n):
        if p[i] == m:
            # Number of elements less than m on the left
            left_less = less_count.get(i, 0)
            # Number of elements greater than m on the right
            right_greater = len(positions) - greater_count.get(i, 0) - 1
            # Total valid subarrays with median m
            result += (left_less + 1) * (right_greater + 1)
    
    return result

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
p = list(map(int, data[2:]))

# Output the result
print(count_median_pairs(n, m, p))