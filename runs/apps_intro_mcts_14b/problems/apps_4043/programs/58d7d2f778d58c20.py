import sys

def solve(n, d, k):
    if d == 1:
        if n <= k + 1:
            print("YES")
            for i in range(2, n + 1):
                print(1, i)
        else:
            print("NO")
        return
    
    if d == 2:
        if n <= 2 * k:
            print("YES")
            for i in range(2, k + 1):
                print(1, i)
            for i in range(k + 1, n + 1):
                print(2, i)
        else:
            print("NO")
        return
    
    if d >= 3:
        if n <= d * (k - 1) + 1:
            print("YES")
            # Create a path of length d
            for i in range(2, d + 1):
                print(1, i)
            
            # Attach the remaining vertices
            current = d + 1
            for i in range(d, 0, -1):
                for _ in range(min(k - 2, n - current)):
                    print(i, current)
                    current += 1
                if current > n:
                    break
        else:
            print("NO")
        return

# Read input
input = sys.stdin.read
data = input().split()
n = int(data[0])
d = int(data[1])
k = int(data[2])

# Solve the problem
solve(n, d, k)