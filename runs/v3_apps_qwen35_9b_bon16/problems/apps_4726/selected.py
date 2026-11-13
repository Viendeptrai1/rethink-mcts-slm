import sys

def solve():
    input_data = sys.stdin.read().strip()
    if not input_data:
        return
    m, n, t = map(int, input_data.split())
    
    if t == 1:
        ops = math.factorial(n)
    elif t == 2:
        ops = 2 ** n
    elif t == 3:
        ops = n ** 4
    elif t == 4:
        ops = n ** 3
    elif t == 5:
        ops = n ** 2
    elif t == 6:
        ops = n * (n.bit_length())
    elif t == 7:
        ops = n
    
    if ops <= m:
        print("AC")
    else:
        print("TLE")

import math
solve()