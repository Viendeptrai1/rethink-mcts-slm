import sys

def find_string(a_00, a_01, a_10, a_11):
    # Check if the given counts are possible
    if a_00 + a_01 != a_00 + a_10 or a_01 + a_11 != a_10 + a_11:
        return "Impossible"
    
    # Calculate the total number of '0's and '1's needed
    total_0 = a_00 + a_01
    total_1 = a_10 + a_11
    
    # If the total number of '0's or '1's is negative, it's impossible
    if total_0 < 0 or total_1 < 0:
        return "Impossible"
    
    # Construct the string
    result = []
    
    # Add '0's and '1's based on the counts
    for _ in range(total_0):
        result.append('0')
    for _ in range(total_1):
        result.append('1')
    
    # Shuffle the string to match the subsequence counts
    # We need to ensure that the counts of '00', '01', '10', '11' are met
    # Start with '00' and '11' first, then '01' and '10'
    
    # Create a copy of the result to shuffle
    shuffled_result = result[:]
    
    # Place '00' and '11'
    for i in range(a_00):
        shuffled_result[i] = '0'
        shuffled_result[i + 1] = '0'
    for i in range(a_11):
        shuffled_result[total_0 + i] = '1'
        shuffled_result[total_0 + i + 1] = '1'
    
    # Place '01' and '10'
    for i in range(a_01):
        shuffled_result[total_0 + a_11 + i] = '0'
        shuffled_result[total_0 + a_11 + i + 1] = '1'
    for i in range(a_10):
        shuffled_result[a_00 + i] = '1'
        shuffled_result[a_00 + i + 1] = '0'
    
    return ''.join(shuffled_result)

# Read input
a_00, a_01, a_10, a_11 = map(int, sys.stdin.readline().split())

# Find and print the result
print(find_string(a_00, a_01, a_10, a_11))