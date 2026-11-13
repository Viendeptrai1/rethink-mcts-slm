def min_dollars_to_win_tournament(n, a):
    # Find the index of your friend
    friend_index = a.index(-1)
    
    # Initialize the total cost to zero
    total_cost = 0
    
    # Calculate the number of rounds
    rounds = n.bit_length() - 1
    
    # Iterate over each round
    for round in range(rounds):
        # Calculate the size of the current group
        group_size = 2 ** (rounds - round)
        
        # Determine the starting index of the group containing your friend
        start_index = (friend_index // group_size) * group_size
        
        # Find the minimum bribe cost in the current group
        min_bribe = float('inf')
        for i in range(start_index, start_index + group_size):
            if i != friend_index:
                min_bribe = min(min_bribe, a[i])
        
        # If your friend is not in the first position, bribe the weaker boxer
        if friend_index % group_size != 0:
            total_cost += min_bribe
        
        # Move your friend to the next round
        friend_index //= 2
    
    return total_cost

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
a = list(map(int, data[1:]))

# Get the result
result = min_dollars_to_win_tournament(n, a)

# Print the result
print(result)