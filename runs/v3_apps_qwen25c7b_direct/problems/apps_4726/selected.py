def check_time_limit(m, n, t):
    if t == 1:
        return "AC" if n <= m else "TLE"
    elif t == 2:
        return "AC" if 2**n <= m else "TLE"
    elif t == 3:
        return "AC" if n**4 <= m else "TLE"
    elif t == 4:
        return "AC" if n**3 <= m else "TLE"
    elif t == 5:
        return "AC" if n**2 <= m else "TLE"
    elif t == 6:
        return "AC" if n * (n.bit_length() - 1) <= m else "TLE"
    elif t == 7:
        return "AC" if n <= m else "TLE"

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
m = int(data[0])
n = int(data[1])
t = int(data[2])
print(check_time_limit(m, n, t))