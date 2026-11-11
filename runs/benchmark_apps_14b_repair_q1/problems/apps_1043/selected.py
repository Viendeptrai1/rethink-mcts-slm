import sys
import heapq

def min_bribe_to_win(n, a):
    # Find the index of the friend
    friend_index = a.index(-1)
    
    # Create a list of tuples (strength, bribe_cost)
    boxers = [(i + 1, cost) for i, cost in enumerate(a)]
    
    # Remove the friend from the list
    boxers.pop(friend_index)
    
    # Min-heap to keep track of the minimum bribe costs
    min_heap = []
    
    # Initialize the heap with the initial boxers
    for strength, cost in boxers:
        heapq.heappush(min_heap, (cost, strength))
    
    total_bribe = 0
    
    # Simulate the tournament stages
    while len(min_heap) > 1:
        # Extract the two weakest boxers
        cost1, strength1 = heapq.heappop(min_heap)
        cost2, strength2 = heapq.heappop(min_heap)
        
        # Determine the winner
        if strength1 < strength2:
            winner_strength = strength1
            winner_cost = cost1
            loser_cost = cost2
        else:
            winner_strength = strength2
            winner_cost = cost2
            loser_cost = cost1
        
        # Add the winner back to the heap
        heapq.heappush(min_heap, (winner_cost, winner_strength))
        
        # Add the bribe cost of the loser
        total_bribe += loser_cost
    
    return total_bribe

# Read input
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

# Calculate and print the result
result = min_bribe_to_win(n, a)
print(result)