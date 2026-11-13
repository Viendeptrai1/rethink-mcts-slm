def max_segments(n, k, a):
    # Convert each number to binary and pad with leading zeros to ensure k bits
    a_binary = [format(num, f'0{k}b') for num in a]
    
    # Initialize variables to keep track of the number of valid segments and the current segment length
    count = 0
    current_length = 0
    
    # Iterate through the binary representation of each number
    for i in range(n):
        # Check if the current bit is different from the previous one
        if i > 0 and a_binary[i][0] != a_binary[i-1][0]:
            # If it's different, increment the current segment length
            current_length += 1
        else:
            # If it's the same, calculate the number of valid segments ending at the previous position
            count += current_length * (current_length + 1) // 2
            # Reset the current segment length
            current_length = 1
    
    # Add the segments from the last segment
    count += current_length * (current_length + 1) // 2
    
    return count

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
k = int(data[1])
a = list(map(int, data[2:]))

# Print the result
print(max_segments(n, k, a))