def min_bribe_cost(n, a):
    # Find the index of the friend boxer
    friend_index = a.index(-1)
    
    # Sort the boxers based on their strength
    sorted_indices = sorted(range(n), key=lambda i: a[i])
    
    # Initialize the total cost
    total_cost = 0
    
    # Iterate through the sorted indices
    for i in range(0, n, 2):
        # If the friend boxer is paired with a weaker boxer, bribe the weaker boxer
        if sorted_indices[i] < friend_index < sorted_indices[i + 1]:
            total_cost += a[sorted_indices[i]]
        elif sorted_indices[i] > friend_index > sorted_indices[i + 1]:
            total_cost += a[sorted_indices[i + 1]]
    
    return total_cost

# Example usage:
# n = int(input())
# a = list(map(int, input().split()))
# print(min_bribe_cost(n, a))