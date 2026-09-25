import sys
from collections import defaultdict

def count_median_pairs(n, m, a):
    # Preprocess the array to count occurrences of values less than, equal to, and greater than m
    less_count = [0] * (n + 1)
    equal_count = [0] * (n + 1)
    greater_count = [0] * (n + 1)
    
    for i in range(n):
        if a[i] < m:
            less_count[i + 1] = less_count[i] + 1
            equal_count[i + 1] = equal_count[i]
            greater_count[i + 1] = greater_count[i]
        elif a[i] == m:
            less_count[i + 1] = less_count[i]
            equal_count[i + 1] = equal_count[i] + 1
            greater_count[i + 1] = greater_count[i]
        else:
            less_count[i + 1] = less_count[i]
            equal_count[i + 1] = equal_count[i]
            greater_count[i + 1] = greater_count[i] + 1
    
    # Count the number of valid subarrays
    count = 0
    for r in range(1, n + 1):
        for l in range(r):
            if (less_count[r] - less_count[l]) <= (equal_count[r] - equal_count[l]) and \
               (equal_count[r] - equal_count[l]) <= (greater_count[r] - greater_count[l]):
                count += 1
    
    return count

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
m = int(data[1])
a = list(map(int, data[2:]))

# Output the result
print(count_median_pairs(n, m, a))