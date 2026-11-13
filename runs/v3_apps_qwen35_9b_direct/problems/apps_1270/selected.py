import sys

def solve():
    try:
        input_data = sys.stdin.read().strip()
        if not input_data:
            return
        n = int(input_data)
    except ValueError:
        return

    if n == 2:
        print(1)
        print(2)
        return

    # To maximize the number of primes, we should use as many 2s as possible.
    # If n is even, we can represent it as n/2 twos.
    # If n is odd, we can represent it as (n-3)/2 twos and one 3.
    # This gives the maximum count because 2 is the smallest prime.

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