def determine_winner(n, a):
    count = sum(1 for x in a if x > 0)
    return "BitLGM" if count % 2 == 1 else "BitAryo"

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

print(determine_winner(n, a))