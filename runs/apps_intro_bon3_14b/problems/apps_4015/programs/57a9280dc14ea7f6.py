import sys

def min_moves(n, m):
    if n == m:
        return 0
    
    moves = 0
    while m > n:
        if m % 2 == 0:
            m //= 2
        elif m % 3 == 0:
            m //= 3
        else:
            return -1
        moves += 1
    
    if m == n:
        return moves
    else:
        return -1

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    m = int(data[1])
    
    result = min_moves(n, m)
    print(result)

if __name__ == "__main__":
    main()