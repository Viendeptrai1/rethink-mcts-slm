import sys
from collections import deque

def max_final_element(N, a):
    # Initialize the deque with the input list
    seq = deque(a)
    
    # Function to get the current state of the sequence
    def get_state():
        return ' '.join(map(str, seq))
    
    # Perform operations until the sequence has only one element
    while len(seq) > 1:
        # Choose the middle element if it's not at either end
        if len(seq) % 2 == 1:
            mid_index = len(seq) // 2
            mid_value = seq[mid_index]
            seq.pop(mid_index)
            seq[0] += mid_value
            seq.popleft()
        else:
            # Otherwise, choose the last element
            last_value = seq[-1]
            seq.pop()
            seq[0] += last_value
            seq.popleft()
        
        # Print the current state of the sequence
        print(get_state())
    
    # Return the final element and the number of operations performed
    return seq[0], len(a) - 1

# Read input
input = sys.stdin.read
data = input().split()
N = int(data[0])
a = list(map(int, data[1:]))

# Get the result
result, operations = max_final_element(N, a)

# Print the result
print(result)
print(operations)
for op in range(operations):
    print(op + 1)