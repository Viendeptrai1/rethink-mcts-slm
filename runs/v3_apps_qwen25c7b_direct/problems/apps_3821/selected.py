import sys
from itertools import combinations

def max_probability(n, probabilities):
    max_prob = 0.0
    for r in range(1, n + 1):
        for combo in combinations(probabilities, r):
            prob = 1.0
            for p in combo:
                prob *= p
            for q in probabilities:
                if q not in combo:
                    prob *= (1 - q)
            max_prob = max(max_prob, prob)
    return max_prob

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    probabilities = list(map(float, data[1:]))
    result = max_probability(n, probabilities)
    print(f"{result:.15f}")