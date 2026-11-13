import sys

def solve_polynomial():
    # Read input
    n, *values = map(int, sys.stdin.readline().split())

    # Function to compute differences
    def compute_differences(seq):
        return [seq[i+1] - seq[i] for i in range(len(seq)-1)]

    # Compute successive differences
    diffs = values
    degree = 0

    while len(set(diffs)) > 1:
        diffs = compute_differences(diffs)
        degree += 1

    # Predict the next value
    if degree == 0:
        next_value = values[0] + (values[1] - values[0])
    else:
        next_value = values[-1]
        for i in range(degree):
            term = diffs[i]
            for j in range(i):
                term *= (n + 1 - j)
            next_value += term

    # Output result
    print(f"{degree} {next_value}")

if __name__ == "__main__":
    solve_polynomial()