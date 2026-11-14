import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    A = int(input_data[0])
    B = int(input_data[1])
    C = int(input_data[2])
    
    g = math.gcd(A, B)
    
    if C % g == 0:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()