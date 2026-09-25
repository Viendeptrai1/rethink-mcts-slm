import sys

def main():
    import sys
    n, m = map(int, sys.stdin.read().split())
    
    if n == m:
        print(0)
        return
    
    moves = 0
    while m % 2 == 0:
        m //= 2
        moves += 1
    while m % 3 == 0:
        m //= 3
        moves += 1
    
    if m == n:
        print(moves)
    else:
        print(-1)

if __name__ == "__main__":
    main()