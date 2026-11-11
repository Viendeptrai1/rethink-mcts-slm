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
                for i in range(n):
                    if i in combo:
                        prob *= ps[i]
                    else:
                        prob *= (1 - ps[i])
                if r == 1:
                    max_prob = max(max_prob, prob)
                elif r == 2:
                    max_prob = max(max_prob, prob)
        return max_prob
    
    n = int(sys.stdin.readline().strip())
    ps = list(map(float, sys.stdin.readline().strip().split()))
    
    result = calculate_probability(ps)
    print(f"{result:.12f}")

if __name__ == "__main__":
    main()