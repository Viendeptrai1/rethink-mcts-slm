import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = []
    for k in range(n):
        a.append(int(input_data[k + 1]))

    # Function f(x) counts the number of set bits (1s) in the binary representation of x
    # f(0) = 0
    # f(2*x) = f(x)  -> shifting left doesn't change bit count
    # f(2*x + 1) = f(x) + 1 -> adding 1 at the end increases bit count by 1
    # This is exactly the population count (Hamming weight)

    from collections import Counter

    counts = Counter()
    ans = 0

    for x in a:
        # Calculate number of set bits
        # Python's bin(x).count('1') is efficient enough for x <= 10^9
        val = bin(x).count('1')
        # Add the number of previous elements with the same f value
        ans += counts[val]
        # Increment the count for this f value
        counts[val] += 1

    print(ans)

if __name__ == "__main__":
    solve()