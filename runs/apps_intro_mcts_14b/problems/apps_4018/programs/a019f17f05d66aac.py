import sys
from collections import Counter

def main():
    import sys
    import math
    from collections import Counter

    def calculate_min_cost(n, k, s):
        # Count the frequency of each character in the string
        freq = Counter(s)
        
        # Calculate the maximum number of distinct subsequences
        max_subsequences = 1
        for count in freq.values():
            max_subsequences *= (count + 1)
        
        # If the maximum number of distinct subsequences is less than k, return -1
        if max_subsequences < k:
            return -1
        
        # Calculate the minimum cost
        cost = 0
        current_subsequences = 1
        for count in sorted(freq.values(), reverse=True):
            while current_subsequences * (count + 1) <= k:
                current_subsequences *= (count + 1)
                cost += n - count
            if current_subsequences == k:
                break
        
        return cost

    # Read input
    n, k = map(int, sys.stdin.readline().split())
    s = sys.stdin.readline().strip()
    
    # Calculate and print the result
    result = calculate_min_cost(n, k, s)
    print(result)

if __name__ == "__main__":
    main()