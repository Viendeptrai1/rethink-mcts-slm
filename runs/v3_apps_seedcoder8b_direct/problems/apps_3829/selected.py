def expected_maximum(m, n):
    # Calculate the expected maximum number of dots after n tosses
    # The expected maximum is the sum of the expected values of the maximums
    # of each toss, which is m/2 for each toss.
    expected_value = 0.0
    for _ in range(n):
        expected_value += m / 2
    return expected_value

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    m, n = map(int, data.split())
    result = expected_maximum(m, n)
    print(f"{result:.12f}")