def find_sequences(n, a):
    from collections import deque

    def is_strictly_increasing(seq):
        return all(x < y for x, y in zip(seq, seq[1:]))

    def is_strictly_decreasing(seq):
        return all(x > y for x, y in zip(seq, seq[1:]))

    # Sort the array to try and find a valid partition
    a.sort()

    # Try to find a partition point
    for i in range(n + 1):
        inc = a[:i]
        dec = a[i:]

        if is_strictly_increasing(inc) and is_strictly_decreasing(dec):
            print("YES")
            print(i)
            print(" ".join(map(str, inc)))
            print(n - i)
            print(" ".join(map(str, dec)))
            return

    print("NO")

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:n+1]))

find_sequences(n, a)