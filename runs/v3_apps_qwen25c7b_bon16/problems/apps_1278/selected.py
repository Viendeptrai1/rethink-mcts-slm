import sys

def earliest_not_so_rainy_day(n, x, y, a):
    stack = []
    min_from_right = [float('inf')] * n
    
    # Calculate the minimum rain amount from the right for each day
    min_from_right[n-1] = a[n-1]
    for i in range(n-2, -1, -1):
        min_from_right[i] = min(a[i], min_from_right[i+1])
    
    # Find the earliest not-so-rainy day
    for i in range(x):
        while stack and a[stack[-1]] >= a[i]:
            stack.pop()
        stack.append(i)
    
    for i in range(n):
        while stack and (i - stack[0] > x or (i + y < n and a[i] >= min_from_right[i+1])):
            stack.pop(0)
        if stack:
            return stack[0] + 1
        while stack and a[stack[-1]] >= a[i]:
            stack.pop()
        stack.append(i)
    
    return n

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
x = int(data[1])
y = int(data[2])
a = list(map(int, data[3:]))

# Output the result
print(earliest_not_so_rainy_day(n, x, y, a))