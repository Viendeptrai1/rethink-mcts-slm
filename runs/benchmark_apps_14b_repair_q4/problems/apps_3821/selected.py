import sys
from itertools import combinations

def main():
    import sys
    import math
    
    def calculate_probability(ps):
        n = len(ps)
        max_prob = 0.0
        for r in range(1, n + 1):
            for combo in combinations(range(n), r):
                prob = 1.0
                for i in combo:
                    prob *= ps[i]
                for i in range(n):
                    if i not in combo:
                        prob *= (1.0 - ps[i])
                max_prob = max(max_prob, prob)
        return max_prob
    
    n = int(sys.stdin.readline())
    ps = list(map(float, sys.stdin.readline().split()))
    
    result = calculate_probability(ps)
    print(f"{result:.12f}")

if __name__ == "__main__":
    main()