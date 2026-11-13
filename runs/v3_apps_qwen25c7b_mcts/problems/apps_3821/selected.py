from itertools import combinations
import sys

def max_probability(n, probabilities):
    max_prob = 0.0
    for r in range(1, n + 1):
        for combo in combinations(probabilities, r):
            prob = 1.0
            for p in combo:
                prob *= p
            for q in [p for p in probabilities if p not in combo]:
                prob *= (1 - q)
            max_prob = max(max_prob, prob)
    return max_prob

if __name__ == "__main__":
    n = int(input().strip())
    probabilities = list(map(float, input().strip().split()))
    result = max_probability(n, probabilities)
    print(f"{result:.15f}")