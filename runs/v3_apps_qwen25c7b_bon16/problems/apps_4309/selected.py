def find_earliest_ABC(N):
    while True:
        if len(set(str(N))) == 1:
            return N
        N += 1

# Read input from standard input
import sys
N = int(sys.stdin.read().strip())

# Find and print the earliest ABC where all digits are the same
print(find_earliest_ABC(N))