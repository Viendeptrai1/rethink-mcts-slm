import sys
import heapq

def min_bribe_to_win(n, a):
    # Find the index of the friend
    friend_index = a.index(-1)
    
    # Create a list of tuples (strength, bribe_cost) excluding the friend
    opponents = [(i + 1, cost) for i, cost in enumerate(a) if cost != -1]
    
    # Sort opponents by their strength
    opponents.sort()
    
    # Initialize the total bribe cost
    total_bribe_cost = 0
    
    # Use a max heap to keep track of the strongest opponents that need to be bribed
    max_heap = []
    
    # Iterate over the opponents
    for strength, cost in opponents:
        # If the current opponent is stronger than the friend, we need to bribe them
        if strength > friend_index + 1:
            # Add the cost to the total bribe cost
            total_bribe_cost += cost
            # Push the negative cost to the max heap (since heapq is a min heap by default)
            heapq.heappush(max_heap, -cost)
        
        # If the heap size exceeds the number of rounds left, remove the weakest opponent that needs to be bribed
        if len(max_heap) > (n.bit_length() - 1):
            heapq.heappop(max_heap)
    
    return total_bribe_cost

# Read input
n = int(sys.stdin.readline())
a = list(map(int, sys.stdin.readline().split()))

# Calculate and print the minimum bribe cost
print(min_bribe_to_win(n, a))