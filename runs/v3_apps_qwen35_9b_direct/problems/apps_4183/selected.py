import sys
import math

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        t = []
        for _ in range(n):
            t.append(int(next(iterator)))
    except StopIteration:
        return

    result = t[0]
    for i in range(1, n):
        result = (result * t[i]) // math.gcd(result, t[i])
    
    print(result)

if __name__ == "__main__":
    solve()