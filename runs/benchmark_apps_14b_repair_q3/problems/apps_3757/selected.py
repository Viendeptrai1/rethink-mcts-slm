import sys

def find_string(a_00, a_01, a_10, a_11):
    # Check if the given counts are possible
    if a_00 + a_01 != a_00 + a_10 or a_01 + a_11 != a_10 + a_11:
        return "Impossible"
    
    # Construct the string
    result = []
    for _ in range(a_11):
        result.append("11")
    for _ in range(a_10 - a_11):
        result.append("10")
    for _ in range(a_01 - a_11):
        result.append("01")
    for _ in range(a_00 - (a_01 - a_11)):
        result.append("00")
    
    # Add remaining "0" and "1" to match the counts
    remaining_0 = a_00 + a_01 - (a_01 - a_11)
    remaining_1 = a_10 + a_11 - (a_10 - a_11)
    
    result.extend(["0"] * remaining_0)
    result.extend(["1"] * remaining_1)
    
    return "".join(result)

# Read input
input_line = sys.stdin.read().strip()
a_00, a_01, a_10, a_11 = map(int, input_line.split())

# Find and print the result
result = find_string(a_00, a_01, a_10, a_11)
print(result)