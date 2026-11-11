import sys

def construct_string(a_00, a_01, a_10, a_11):
    # Check if the given counts can form a valid string
    if a_00 + a_01 != a_00 + a_10 or a_01 + a_11 != a_10 + a_11:
        return "Impossible"
    
    # Initialize the result string
    result = []
    
    # Add '0's and '1's based on the counts
    for _ in range(a_00):
        result.append('0')
        result.append('0')
    for _ in range(a_01):
        result.append('0')
        result.append('1')
    for _ in range(a_10):
        result.append('1')
        result.append('0')
    for _ in range(a_11):
        result.append('1')
        result.append('1')
    
    # Shuffle the result to ensure the order is correct
    from random import shuffle
    shuffle(result)
    
    return ''.join(result)

# Read input
a_00, a_01, a_10, a_11 = map(int, sys.stdin.read().split())

# Construct and print the result
print(construct_string(a_00, a_01, a_10, a_11))