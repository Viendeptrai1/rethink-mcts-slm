import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    K = int(input_data[1])

    remainder = N % K
    ans = min(remainder, K - remainder)
    print(ans)

if __name__ == "__main__":
    solve()