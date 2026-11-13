import sys

def max_monsters_defeated(N, A, B):
    total = 0
    for i in range(N):
        if A[i] + A[i + 1] <= B[i]:
            total += A[i] + A[i + 1]
        else:
            total += min(B[i], A[i]) + min(B[i] - min(B[i], A[i]), A[i + 1])
    return total

# Read input
input = sys.stdin.read
data = input().split()
N = int(data[0])
A = list(map(int, data[1:N+2]))
B = list(map(int, data[N+2:]))

# Calculate and print the result
result = max_monsters_defeated(N, A, B)
print(result)