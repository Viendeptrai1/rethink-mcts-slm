def can_make_increasing(n, m, a, b):
    # Check if swapping elements can make both matrices increasing
    for i in range(n):
        for j in range(m):
            if a[i][j] > b[i][j]:
                a[i][j], b[i][j] = b[i][j], a[i][j]
    
    # Check if the first matrix is increasing
    for i in range(n):
        for j in range(1, m):
            if a[i][j] <= a[i][j - 1]:
                return "Impossible"
    
    for j in range(m):
        for i in range(1, n):
            if a[i][j] <= a[i - 1][j]:
                return "Impossible"
    
    # Check if the second matrix is increasing
    for i in range(n):
        for j in range(1, m):
            if b[i][j] <= b[i][j - 1]:
                return "Impossible"
    
    for j in range(m):
        for i in range(1, n):
            if b[i][j] <= b[i - 1][j]:
                return "Impossible"
    
    return "Possible"

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])

a = []
for i in range(n):
    a.append(list(map(int, data[2 + i * m : 2 + (i + 1) * m])))

b = []
for i in range(n):
    b.append(list(map(int, data[2 + n * m + i * m : 2 + n * m + (i + 1) * m])))

# Output result
print(can_make_increasing(n, m, a, b))