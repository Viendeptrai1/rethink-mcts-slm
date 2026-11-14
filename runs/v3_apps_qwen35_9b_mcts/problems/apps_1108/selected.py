import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    n = int(next(iterator))
    
    count = 0
    for _ in range(n):
        p = int(next(iterator))
        q = int(next(iterator))
        if q - p >= 2:
            count += 1
            
    print(count)

if __name__ == "__main__":
    solve()