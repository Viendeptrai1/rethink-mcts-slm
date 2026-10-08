def min_additional_problems(n, m, a, b):
    a.sort()
    b.sort()
    
    additional_problems = 0
    j = 0
    
    for i in range(n):
        while j < m and b[j] < a[i]:
            j += 1
        if j == m:
            additional_problems += 1
        else:
            j += 1
    
    return additional_problems

# Reading input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
a = list(map(int, data[2:2+n]))
b = list(map(int, data[2+n:]))

# Output the result
print(min_additional_problems(n, m, a, b))