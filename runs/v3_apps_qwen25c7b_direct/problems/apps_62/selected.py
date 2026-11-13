def determine_winner(n, a):
    min_val = min(a)
    total_sum = sum(a)
    
    if total_sum % 2 == 0:
        return "BitAryo"
    else:
        return "BitLGM"

# Example usage:
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

print(determine_winner(n, a))