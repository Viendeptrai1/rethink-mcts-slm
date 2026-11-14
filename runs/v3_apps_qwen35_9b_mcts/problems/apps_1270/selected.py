import sys

def solve():
    try:
        input_data = sys.stdin.read().strip()
        if not input_data:
            return
        n = int(input_data)
    except ValueError:
        return

    if n % 2 == 0:
        k = n // 2
        primes = [2] * k
    else:
        k = (n - 3) // 2 + 1
        primes = [2] * k
        primes[-1] = 3

    print(k)
    print(*(primes))

if __name__ == "__main__":
    solve()