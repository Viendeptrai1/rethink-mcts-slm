import sys

def count_missed_trains(s):
    # Convert the binary string to an integer
    s_decimal = int(s, 2)
    
    # Initialize the count of missed trains
    missed_trains = 0
    
    # Iterate over possible values of k
    k = 0
    while 4**k < s_decimal:
        missed_trains += 1
        k += 1
    
    return missed_trains

# Read input from standard input
s = sys.stdin.read().strip()

# Output the result
print(count_missed_trains(s))