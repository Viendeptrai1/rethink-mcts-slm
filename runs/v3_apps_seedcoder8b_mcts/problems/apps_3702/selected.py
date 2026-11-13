def find_arithmetic_sequence(n, a, d):
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    n = int(data[0])
    a = int(data[1])
    d = int(data[2])

    # Precompute Fibonacci numbers up to a large limit
    def fibonacci_up_to(limit):
        fibs = [0, 1]
        while True:
            next_fib = fibs[-1] + fibs[-2]
            if next_fib > limit:
                break
            fibs.append(next_fib)
        return fibs

    # Calculate the maximum possible value for b and e
    max_b = 2**64
    max_e = 2**64

    # Generate the sequence a + i * d
    sequence_a = [a + i * d for i in range(n)]

    # Convert sequence_a to strings for substring checking
    sequence_a_str = [str(x) for x in sequence_a]

    # Precompute Fibonacci numbers up to a large limit
    # We need to check the last 18 digits of Fibonacci numbers
    limit = 10**18
    fibs = fibonacci_up_to(limit)

    # Convert Fibonacci numbers to strings for substring checking
    fibs_str = [str(fib) for fib in fibs]

    # Try to find b and e
    for b in range(1, max_b):
        for e in range(1, max_e):
            valid = True
            for i in range(n):
                fib_index = b + i * e
                if fib_index >= len(fibs_str):
                    valid = False
                    break
                fib_str = fibs_str[fib_index]
                if not any(sub in fib_str[-18:] for sub in sequence_a_str):
                    valid = False
                    break
            if valid:
                print(b, e)
                return

    print(-1)