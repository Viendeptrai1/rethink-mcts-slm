import sys

# Read input from stdin
w = int(sys.stdin.read().strip())

# Check if the weight is even and greater than 2
if w % 2 == 0 and w > 2:
    print("YES")
else:
    print("NO")