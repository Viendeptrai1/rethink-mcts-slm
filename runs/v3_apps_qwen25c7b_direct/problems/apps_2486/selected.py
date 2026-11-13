import sys
from typing import List

def count_unnecessary_cards(N: int, K: int, a: List[int]) -> int:
    # Initialize a list to keep track of whether each card is unnecessary
    unnecessary = [False] * N
    
    # Iterate over each card
    for i in range(N):
        # Create a new list excluding the current card
        remaining_cards = a[:i] + a[i+1:]
        
        # Check if there exists a good subset in the remaining cards
        found_good_subset = False
        for j in range(1 << len(remaining_cards)):
            subset_sum = 0
            for k in range(len(remaining_cards)):
                if j & (1 << k):
                    subset_sum += remaining_cards[k]
            if subset_sum >= K:
                found_good_subset = True
                break
        
        # If no good subset exists in the remaining cards, the current card is unnecessary
        if not found_good_subset:
            unnecessary[i] = True
    
    # Return the number of unnecessary cards
    return sum(unnecessary)

# Read input from standard input
input = sys.stdin.read
data = input().split()

N = int(data[0])
K = int(data[1])
a = list(map(int, data[2:]))

# Call the function and print the result
print(count_unnecessary_cards(N, K, a))