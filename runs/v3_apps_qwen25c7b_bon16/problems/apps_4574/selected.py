import sys
from collections import Counter

def max_rectangle_area(N, lengths):
    lengths.sort()
    count = Counter(lengths)
    max_area = 0
    
    for i in range(len(lengths) - 1):
        for j in range(i + 1, len(lengths)):
            if lengths[i] != lengths[j]:
                if count[lengths[i]] >= 2 and count[lengths[j]] >= 2:
                    max_area = max(max_area, lengths[i] * lengths[j])
    
    return max_area

# Read input
input = sys.stdin.read
data = input().split()

N = int(data[0])
lengths = list(map(int, data[1:]))

# Calculate and print the result
print(max_rectangle_area(N, lengths))