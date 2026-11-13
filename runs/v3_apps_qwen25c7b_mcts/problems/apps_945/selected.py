def check_self_intersections(n, points):
    stack = []
    
    for i in range(n):
        while len(stack) >= 2 and points[i] < points[stack[-1]]:
            j = stack.pop()
            if points[j] <= points[stack[-1]]:
                return "yes"
        stack.append(i)
    
    return "no"

# Input reading
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
points = list(map(int, data[1:]))

# Output result
print(check_self_intersections(n, points))