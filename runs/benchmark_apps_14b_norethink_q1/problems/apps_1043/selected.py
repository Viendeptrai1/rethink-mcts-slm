import sys
import heapq

def min_bribe_to_win(n, a):
    # Find the index of the friend
    friend_index = a.index(-1)
    
    # Create a list of tuples (strength, bribe_cost)
    boxers = [(i + 1, a[i]) for i in range(n)]
    
    # Remove the friend from the list
    friend_strength = boxers.pop(friend_index)[0]
    
    # Sort the boxers by their strength
    boxers.sort()
    
    # Initialize the total cost
    total_cost = 0
    
    # Simulate the tournament
    while len(boxers) > 0:
        # Pair the friend with the weakest opponent he can beat
        opponent = boxers.pop(0)
        
        # If the opponent's strength is greater than the friend's, we need to bribe
        if opponent[0] > friend_strength:
            total_cost += opponent[1]
        else:
            # Otherwise, the friend beats the opponent without a bribe
            pass
    
    return total_cost

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

# Output the result
print(min_bribe_to_win(n, a))