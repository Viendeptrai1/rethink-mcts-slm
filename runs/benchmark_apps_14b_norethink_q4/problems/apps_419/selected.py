import sys

def count_missed_trains(s):
    # Convert the binary string to an integer
    s = int(s, 2)
    
    # Initialize the count of missed trains
    count = 0
    
    # Iterate over powers of 4
    power_of_4 = 1
    while power_of_4 < s:
        count += 1
        power_of_4 *= 4
    
    return count

# Read input from standard input
s = sys.stdin.read().strip()

# Output the result
print(count_missed_trains(s))