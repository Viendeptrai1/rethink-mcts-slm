def min_instability(n, a):
    a.sort()
    return min(a[i+1] - a[i] for i in range(n-1))

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

print(min_instability(n, a))