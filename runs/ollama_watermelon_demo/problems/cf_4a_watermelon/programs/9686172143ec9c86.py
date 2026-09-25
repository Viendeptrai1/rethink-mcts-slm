import sys

# Read input from stdin
w = int(sys.stdin.read().strip())

# Check if the watermelon can be divided into two even parts
if w % 2 == 0 and w > 2:
    print("YES")
else:
    print("NO")