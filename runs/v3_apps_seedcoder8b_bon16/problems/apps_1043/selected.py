def min_cost_to_win_tournament(n, a):
    # Find the index of your friend
    friend_index = a.index(-1)
    
    # Initialize the cost
    total_cost = 0
    
    # We need to bring the friend to the top of the tournament
    current_power = n
    
    while current_power > 1:
        pair_size = current_power // 2
        
        # Determine which pair the friend is currently in
        current_pair = friend_index // pair_size
        
        # Find the stronger opponent in the current pair
        first_in_pair = current_pair * pair_size
        second_in_pair = first_in_pair + 1
        
        if a[first_in_pair] != -1 and a[second_in_pair] != -1:
            if a[first_in_pair] > a[second_in_pair]:
                stronger_index = first_in_pair
            else:
                stronger_index = second_in_pair
        elif a[first_in_pair] == -1:
            stronger_index = second_in_pair
        else:
            stronger_index = first_in_pair
        
        # If the friend is stronger, he wins this stage
        if stronger_index == friend_index:
            # Move to the next stage
            current_power = pair_size
            friend_index = current_pair
        else:
            # The friend must be bribed
            total_cost += a[stronger_index]
            # Move to the next stage
            current_power = pair_size
            friend_index = current_pair
    
    return total_cost

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    a = list(map(int, data[1:n+1]))
    
    result = min_cost_to_win_tournament(n, a)
    print(result)