def count_missed_trains(s):
    s_int = int(s, 2)
    k = 0
    count = 0
    while 4**k < s_int:
        count += 1
        k += 1
    return count

# Example usage:
import sys
input = sys.stdin.read().strip()
print(count_missed_trains(input))