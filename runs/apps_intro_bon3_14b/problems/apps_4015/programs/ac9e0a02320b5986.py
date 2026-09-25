import sys

def count_moves(n, m):
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
    result = count_moves(n, m)
    print(result)

if __name__ == "__main__":
    main()