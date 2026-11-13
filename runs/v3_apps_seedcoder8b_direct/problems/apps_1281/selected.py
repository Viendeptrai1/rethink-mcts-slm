def max_liked_segments(n, k, a):
    # Function to calculate the maximum number of segments with XOR not equal to 0
    # after performing the allowed operations.

    # Initialize the prefix XOR array
    prefix_xor = [0] * (n + 1)
    
    # Calculate prefix XOR for the array
    for i in range(1, n + 1):
        prefix_xor[i] = prefix_xor[i - 1] ^ a[i - 1]
    
    # Set to store unique prefix XOR values
    unique_xor = set()
    
    # Add all prefix XOR values to the set
    for xor_value in prefix_xor:
        unique_xor.add(xor_value)
    
    # The maximum number of segments is the number of unique prefix XOR values
    # plus the number of elements in the array (since each element can be a segment)
    return len(unique_xor) + n

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Parse input
n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:2 + n]))

# Get the result
result = max_liked_segments(n, k, a)

# Print the result
print(result)