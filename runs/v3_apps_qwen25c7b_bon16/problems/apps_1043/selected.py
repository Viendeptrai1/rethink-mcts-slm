import sys
from typing import List

def min_bribe_cost(n: int, strengths: List[int]) -> int:
    # Find the index of the friend
    friend_index = strengths.index(-1)
    # Sort the strengths array except for the friend's strength
    sorted_strengths = sorted(strengths[:friend_index] + strengths[friend_index+1:])
    total_cost = 0
    
    # Iterate over the sorted strengths array in reverse order
    for i in range(len(sorted_strengths) // 2):
        # Pair the current boxer with the weakest boxer that hasn't been paired yet
        total_cost += sorted_strengths[i]
    
    return total_cost

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
strengths = list(map(int, data[1:]))

# Calculate and print the result
print(min_bribe_cost(n, strengths))