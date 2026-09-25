import sys

def count_blue_balls(N, A, B):
    # Calculate the length of one complete cycle
    cycle_length = A + B
    
    # Determine how many complete cycles fit into N
    complete_cycles = N // cycle_length
    
    # Calculate the number of blue balls in complete cycles
    blue_in_complete_cycles = complete_cycles * A
    
    # Calculate the remaining balls after complete cycles
    remaining_balls = N % cycle_length
    
    # Calculate the number of blue balls in the remaining part
    blue_in_remaining = min(remaining_balls, A)
    
    # Total number of blue balls
    total_blue_balls = blue_in_complete_cycles + blue_in_remaining
    
    return total_blue_balls

# Read input
input_data = sys.stdin.read().split()
N = int(input_data[0])
A = int(input_data[1])
B = int(input_data[2])

# Calculate and print the result
result = count_blue_balls(N, A, B)
print(result)