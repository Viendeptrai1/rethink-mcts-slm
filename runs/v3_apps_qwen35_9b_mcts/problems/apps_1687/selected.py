import sys
import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = []
    for i in range(n):
        a.append(int(input_data[i + 1]))
    
    current_gcd = a[0]
    for i in range(1, n):
        current_gcd = gcd(current_gcd, a[i])
        if current_gcd == 1:
            break
    
    if current_gcd in a:
        print(current_gcd)
    else:
        print(-1)

if __name__ == "__main__":
    solve()