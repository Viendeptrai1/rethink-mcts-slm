import sys

def min_bribe_to_win(n, a):
    # Find the index of the friend
    friend_index = a.index(-1)
    
    # Sort the boxers by their strength, excluding the friend
    sorted_boxers = sorted((strength, i) for i, strength in enumerate(a) if strength != -1)
    
    # Initialize the total cost
    total_cost = 0
    
    # Simulate the tournament stages
    while len(sorted_boxers) > 1:
        next_round = []
        for i in range(0, len(sorted_boxers), 2):
            # Get the strengths and indices of the two boxers in the pair
            strength1, index1 = sorted_boxers[i]
            strength2, index2 = sorted_boxers[i + 1]
            
            # Determine the winner
            if index1 == friend_index or (index1 != friend_index and strength1 > strength2):
                winner_strength, winner_index = strength1, index1
                loser_strength, loser_index = strength2, index2
            else:
                winner_strength, winner_index = strength2, index2
                loser_strength, loser_index = strength1, index1
            
            # If the friend is not the winner, add the cost of bribing the loser
            if winner_index != friend_index:
                total_cost += a[loser_index]
            
            # Add the winner to the next round
            next_round.append((winner_strength, winner_index))
        
        # Move to the next round
        sorted_boxers = next_round
    
    return total_cost

# Read input
n = int(sys.stdin.readline())
a = list(map(int, sys.stdin.readline().split()))

# Calculate and print the result
print(min_bribe_to_win(n, a))