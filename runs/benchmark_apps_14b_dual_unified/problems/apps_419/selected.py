import sys

def count_missed_trains(s):
    # Convert binary string to decimal integer
    s_decimal = int(s, 2)
    
    # Initialize count of missed trains
    missed_trains = 0
    
    # Iterate over powers of 4
    power_of_4 = 1
    while power_of_4 < s_decimal:
        missed_trains += 1
        power_of_4 *= 4
    
    return missed_trains

# Read input from standard input
s = sys.stdin.read().strip()

# Output the result
print(count_missed_trains(s))