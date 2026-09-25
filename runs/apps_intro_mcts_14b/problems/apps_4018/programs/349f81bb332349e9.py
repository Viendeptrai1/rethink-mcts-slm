import sys
from collections import Counter

def main():
    import sys
    import math
    
    def calculate_max_subsequences(n, char_count):
        max_subsequences = 1
        for count in char_count.values():
            max_subsequences *= (count + 1)
        return max_subsequences - 1  # Subtract 1 to exclude the empty subsequence
    
    def calculate_min_cost(n, k, char_count):
        max_subsequences = calculate_max_subsequences(n, char_count)
        if k > max_subsequences:
            return -1
        
        # Calculate the minimum cost to get k distinct subsequences
        cost = 0
        current_subsequences = 0
        for count in sorted(char_count.values(), reverse=True):
            if current_subsequences + count >= k:
                additional_needed = k - current_subsequences
                cost += n - (n - count) * (additional_needed // count)
                break
            cost += n - count
            current_subsequences += count
        
        return cost
    
    # Read input
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    s = data[2]
    
    # Count the frequency of each character in the string
    char_count = Counter(s)
    
    # Calculate the minimum cost
    result = calculate_min_cost(n, k, char_count)
    
    # Print the result
    print(result)

if __name__ == "__main__":
    main()