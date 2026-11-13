import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    k = int(input_data[1])

    remainder = n % k
    if remainder < k - remainder:
        print(remainder)
    else:
        print(k - remainder)

if __name__ == "__main__":
    solve()