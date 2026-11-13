def min_moves_to_divisible_by_25(n):
    s = str(n)
    length = len(s)
    
    # Check if the number is already divisible by 25
    if int(s[-2:]) % 25 == 0:
        return 0
    
    # Find the positions of '0' and '5'
    pos_0 = s.find('0')
    pos_5 = s.find('5')
    
    # If both '0' and '5' are found, calculate the minimum moves
    if pos_0 != -1 and pos_5 != -1:
        # Move '0' next to '5'
        if pos_0 > pos_5:
            moves = pos_0 - pos_5 - 1 + pos_0
        else:
            moves = pos_5 - pos_0 - 1 + pos_5
        
        # Ensure there are no leading zeros after the move
        if pos_0 < pos_5:
            moves += sum(1 for i in range(pos_0 + 1, pos_5) if s[i] == '0')
        else:
            moves += sum(1 for i in range(pos_5 + 1, pos_0) if s[i] == '0')
        
        return moves
    
    # If either '0' or '5' is not found, check for the closest pair
    elif pos_0 != -1:
        # Find the closest '5' to the right of '0'
        closest_5 = s.find('5', pos_0 + 1)
        if closest_5 != -1:
            moves = closest_5 - pos_0 - 1 + closest_5
            return moves
    
    elif pos_5 != -1:
        # Find the closest '0' to the right of '5'
        closest_0 = s.find('0', pos_5 + 1)
        if closest_0 != -1:
            moves = closest_0 - pos_5 - 1 + closest_0
            return moves
    
    # If neither '0' nor '5' is found, it's impossible to make the number divisible by 25
    return -1

# Example usage
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    result = min_moves_to_divisible_by_25(n)
    print(result)