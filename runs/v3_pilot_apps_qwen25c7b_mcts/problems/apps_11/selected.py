def max_chocolates(n, a, b, p, q):
    count_a = n // a
    count_b = n // b
    count_ab = n // (a * b)
    
    red_chocolates = count_a * p + (count_ab - count_ab) * p
    blue_chocolates = count_b * q + (count_ab - count_ab) * q
    
    return max(red_chocolates, blue_chocolates)

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = int(data[1])
b = int(data[2])
p = int(data[3])
q = int(data[4])

print(max_chocolates(n, a, b, p, q))