import sys
from collections import Counter

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    n = int(data[0])
    a = []
    idx = 1
    for _ in range(n):
        a.append(int(data[idx]))
        idx += 1

    # Precompute f(x) for each number in the sequence
    # f(x) is the number of set bits (popcount) in x
    # We can compute this efficiently using bin(x).count('1')
    
    counts = Counter()
    for x in a:
        # f(x) is the number of 1s in binary representation of x
        fx = bin(x).count('1')
        counts[fx] += 1

    ans = 0
    for count in counts.values():
        if count > 1:
            # Number of pairs from count items is count * (count - 1) // 2
            ans += count * (count - 1) // 2

    print(ans)

if __name__ == "__main__":
    solve()