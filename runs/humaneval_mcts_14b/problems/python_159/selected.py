def eat(number, need, remaining):
    # Calculate the total number of carrots needed
    total_needed = number + need
    
    # Determine how many carrots can actually be eaten
    if remaining >= need:
        # If there are enough remaining carrots to meet the need
        total_eaten = total_needed
        carrots_left = remaining - need
    else:
        # If there are not enough remaining carrots
        total_eaten = number + remaining
        carrots_left = 0
    
    return [total_eaten, carrots_left]

# Example usage:
# print(eat(5, 6, 10))  # Output: [11, 4]
# print(eat(4, 8, 9))   # Output: [12, 1]
# print(eat(1, 10, 10)) # Output: [11, 0]
# print(eat(2, 11, 5))  # Output: [7, 0]