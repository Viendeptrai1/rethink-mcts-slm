def find_string(a_00, a_01, a_10, a_11):
    # Check if the sum of all pairs is valid
    if a_00 + a_01 + a_10 + a_11 == 0:
        return "Impossible"
    
    # Check if the sum of pairs (01 and 10) is equal
    if a_01 != a_10:
        return "Impossible"
    
    # Check if the sum of pairs (00 and 11) is equal
    if a_00 != a_11:
        return "Impossible"
    
    # If both conditions are satisfied, construct the string
    # The string should have a_00 '00' pairs, a_01 '01' pairs, and a_11 '11' pairs
    # We can interleave '0' and '1' to form the required pairs
    result = []
    
    # Add '00' pairs
    for _ in range(a_00):
        result.append('00')
    
    # Add '01' pairs
    for _ in range(a_01):
        result.append('01')
    
    # Add '11' pairs
    for _ in range(a_11):
        result.append('11')
    
    # Add '10' pairs
    for _ in range(a_10):
        result.append('10')
    
    # Join the list into a single string
    return ''.join(result)

# Read input
a_00, a_01, a_10, a_11 = map(int, input().split())

# Find and print the result
print(find_string(a_00, a_01, a_10, a_11))