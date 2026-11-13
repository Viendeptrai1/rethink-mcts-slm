def find_string(a_00, a_01, a_10, a_11):
    total_pairs = a_00 + a_01 + a_10 + a_11
    max_length = 2 * total_pairs
    
    if max_length > 1000000:
        return "Impossible"
    
    result = []
    
    # Add '00' pairs
    result.extend(['00'] * a_00)
    
    # Add '01' pairs
    result.extend(['01'] * a_01)
    
    # Add '10' pairs
    result.extend(['10'] * a_10)
    
    # Add '11' pairs
    result.extend(['11'] * a_11)
    
    # Flatten the list and join into a string
    return ''.join(result)

# Read input
a_00, a_01, a_10, a_11 = map(int, input().split())

# Find and print the result
print(find_string(a_00, a_01, a_10, a_11))