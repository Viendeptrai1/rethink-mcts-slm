import sys

def solve_probability():
    n = int(sys.stdin.readline().strip())
    probabilities = list(map(float, sys.stdin.readline().split()))

    max_prob = max(probabilities)
    total_prob = sum(probabilities)

    result = 0
    for p in probabilities:
        if p == max_prob:
            result = max(result, max_prob)
        else:
            result = max(result, 1 - (1 - max_prob) / (1 - p))

    print(f"{result:.12f}")

solve_probability()