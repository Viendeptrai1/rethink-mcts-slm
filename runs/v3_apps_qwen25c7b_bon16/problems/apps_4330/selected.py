def find_integer(K):
    return "IMPOSSIBLE"

# Read input from stdin
import sys
input = sys.stdin.read().strip()
A, B = map(int, input.split())

# Calculate the midpoint between A and B
K = (A + B) // 2

# Check if K satisfies the condition |A - K| = |B - K|
if abs(A - K) == abs(B - K):
    print(K)
else:
    print(find_integer(K))