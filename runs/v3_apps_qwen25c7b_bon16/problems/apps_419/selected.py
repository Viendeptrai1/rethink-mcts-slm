def count_missed_trains(s):
    # Convert binary string to integer
    s_int = int(s, 2)
    
    # Initialize count of missed trains
    count = 0
    
    # Iterate through powers of 4 until 4^k exceeds or equals s
    k = 0
    while 4**k < s_int:
        count += 1
        k += 1
    
    return count

# Input handling
import sys
input_line = sys.stdin.read().strip()
print(count_missed_trains(input_line))