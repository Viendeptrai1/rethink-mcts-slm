import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = []
    for i in range(n):
        a.append(int(input_data[i+1]))

    # Function f(x) counts the number of set bits (1s) in binary representation of x
    def f(x):
        count = 0
        while x > 0:
            if x & 1:
                count += 1
            x >>= 1
        return count

    # Count frequencies of f(a_i)
    freq = {}
    for x in a:
        val = f(x)
        freq[val] = freq.get(val, 0) + 1

    # Calculate number of pairs
    ans = 0
    for count in freq.values():
        if count > 1:
            ans += count * (count - 1) // 2

    print(ans)

if __name__ == "__main__":
    solve()