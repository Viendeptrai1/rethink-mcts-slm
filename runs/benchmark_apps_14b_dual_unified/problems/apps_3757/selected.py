import sys

def construct_string(a_00, a_01, a_10, a_11):
    # Check if the given counts can form a valid string
    if a_00 + a_01 + a_10 + a_11 == 0:
        return "Impossible"
    
    # Calculate the total number of '0's and '1's needed
    total_0 = a_00 + a_01
    total_1 = a_10 + a_11
    
    # If the total number of '0's or '1's is negative, it's impossible
    if total_0 < 0 or total_1 < 0:
        return "Impossible"
    
    # Start constructing the string
    result = []
    
    # Add '11' subsequences
    for _ in range(a_11):
        result.append('1')
        result.append('1')
    
    # Add '01' subsequences
    for _ in range(a_01):
        result.append('0')
        result.append('1')
    
    # Add '10' subsequences
    for _ in range(a_10):
        result.append('1')
        result.append('0')
    
    # Add '00' subsequences
    for _ in range(a_00):
        result.append('0')
        result.append('0')
    
    # Check if the constructed string has the correct number of '0's and '1's
    if result.count('0') != total_0 or result.count('1') != total_1:
        return "Impossible"
    
    return ''.join(result)

# Read input
input_line = sys.stdin.read().strip()
a_00, a_01, a_10, a_11 = map(int, input_line.split())

# Output the result
print(construct_string(a_00, a_01, a_10, a_11))