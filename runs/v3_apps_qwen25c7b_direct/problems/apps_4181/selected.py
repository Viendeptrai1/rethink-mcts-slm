import sys

def max_monsters_defeated(N, A, B):
    max_defeated = 0
    for i in range(N):
        max_defeated += min(A[i], B[i])
        if i < N - 1:
            max_defeated += min(A[i + 1], B[i])
    return max_defeated

# Read input
input = sys.stdin.read
data = input().split()

N = int(data[0])
A = list(map(int, data[1:N+2]))
B = list(map(int, data[N+2:]))

# Calculate and print the result
print(max_monsters_defeated(N, A, B))