import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    N = int(input_data[0])
    K = int(input_data[1])

    if N == 0:
        print(0)
        return

    # We can reduce N by repeatedly subtracting K until it's less than K.
    # This is equivalent to N % K.
    r = N % K

    # After reaching r, one more operation gives |r - K| = K - r.
    # We take the minimum of r and K - r.
    ans = min(r, K - r)
    print(ans)

if __name__ == "__main__":
    solve()