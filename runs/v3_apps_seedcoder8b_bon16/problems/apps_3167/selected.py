import sys
from collections import defaultdict

def solve():
    N, K = map(int, input().split())
    X = list(map(int, input().split()))
    Q = int(input())

    # Initialize a dictionary to store the difference array
    diff = defaultdict(int)

    # Process the K calls to the something procedure
    for jump in X:
        i = 0
        while i < N:
            diff[i] += 1
            i += jump

    # Calculate prefix sums
    prefix_sum = [0] * (N + 1)
    for i in range(1, N + 1):
        prefix_sum[i] = prefix_sum[i-1] + diff[i-1]

    # Process the Q queries
    for _ in range(Q):
        L, R = map(int, input().split())
        print(prefix_sum[R + 1] - prefix_sum[L])

solve()