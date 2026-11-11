import sys

def count_triples(N, K):
    # Initialize a list to count occurrences of each remainder when divided by K
    remainder_count = [0] * K
    
    # Count the occurrences of each remainder for numbers from 1 to N
    for i in range(1, N + 1):
        remainder_count[i % K] += 1
    
    # Initialize the result counter
    result = 0
    
    # Iterate over all possible remainders for a, b, and c
    for r_a in range(K):
        for r_b in range(K):
            for r_c in range(K):
                # Check if the sums a+b, b+c, and c+a are multiples of K
                if (r_a + r_b) % K == 0 and (r_b + r_c) % K == 0 and (r_c + r_a) % K == 0:
                    # Multiply the counts of each remainder to get the number of valid triples
                    result += remainder_count[r_a] * remainder_count[r_b] * remainder_count[r_c]
    
    return result

# Read input from standard input
N, K = map(int, sys.stdin.read().split())

# Print the result
print(count_triples(N, K))