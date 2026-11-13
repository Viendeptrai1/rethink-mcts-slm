import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = []
    for i in range(n):
        a.append(int(input_data[i+1]))

    # For each number, count how many times it can be divided by 2.
    # Multiplying by 3 does not affect the power of 2 in the prime factorization.
    # So the total operations is the sum of the exponent of 2 in the prime factorization of each a_i.
    total_ops = 0
    for x in a:
        count = 0
        while x % 2 == 0:
            x //= 2
            count += 1
        total_ops += count

    print(total_ops)

if __name__ == "__main__":
    solve()