import sys
from collections import defaultdict
from math import gcd

def solve():
    N = int(sys.stdin.readline())
    points = [tuple(map(int, sys.stdin.readline().split())) for _ in range(N)]
    
    if N <= 2:
        print("success")
        return
    
    lines = defaultdict(set)
    for i in range(N):
        for j in range(i+1, N):
            x1, y1 = points[i]
            x2, y2 = points[j]
            if x1 == x2:
                line = ('v', x1)
            else:
                dx, dy = x2 - x1, y2 - y1
                g = gcd(dx, dy)
                dx, dy = dx // g, dy // g
                if dx < 0:
                    dx, dy = -dx, -dy
                line = ('s', dy, dx, y1 - dy * x1)
            lines[line].add(i)
            lines[line].add(j)
    
    if len(lines) == 1:
        print("success")
        return
    
    for line in lines:
        remaining = N - len(lines[line])
        if remaining <= 1:
            print("success")
            return
    
    print("failure")

if __name__ == "__main__":
    solve()