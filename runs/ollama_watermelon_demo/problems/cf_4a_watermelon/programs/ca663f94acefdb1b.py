import sys

# Read input from stdin
w = int(sys.stdin.read().strip())

# Check if the watermelon weight can be divided into two even parts
if w > 2 and w % 2 == 0:
    print("YES")
else:
    print("NO")