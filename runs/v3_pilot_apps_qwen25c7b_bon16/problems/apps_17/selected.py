def mexican_wave_spectators(n, k, t):
    if t <= k:
        return t
    elif t <= n:
        return k
    else:
        return n - ((t - n) % (n - k))

# Example usage
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
t = int(data[2])
print(mexican_wave_spectators(n, k, t))