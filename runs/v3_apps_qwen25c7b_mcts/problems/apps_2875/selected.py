def find_reversal_indices(cards):
    n = len(cards)
    sorted_cards = sorted(cards)
    
    # Find the first index where the original and sorted arrays differ
    start = next((i for i in range(n) if cards[i] != sorted_cards[i]), None)
    
    # If the entire array is already sorted, return "impossible"
    if start is None:
        return "impossible"
    
    # Find the last index where the original and sorted arrays differ
    end = next((i for i in range(n-1, -1, -1) if cards[i] != sorted_cards[i]), None)
    
    # Check if reversing the subarray from start to end sorts the array
    reversed_subarray = cards[start:end+1][::-1]
    if cards[:start] + reversed_subarray + cards[end+1:] == sorted_cards:
        return f"{start+1} {end+1}"
    
    return "impossible"

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
cards = list(map(int, data[1:]))

result = find_reversal_indices(cards)
print(result)