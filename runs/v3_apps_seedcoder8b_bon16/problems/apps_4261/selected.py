import sys

def solve():
    A, B, C = map(int, sys.stdin.readline().split())
    remaining = C - min(C, A - B)
    print(remaining)

solve()