def eat(number, need, remaining):
    if need <= remaining:
        total_eaten = number + need
        carrots_left = remaining - need
    else:
        total_eaten = number + remaining
        carrots_left = 0
    
    return [total_eaten, carrots_left]

# Example usage:
# print(eat(5, 6, 10))  # Output: [11, 4]
# print(eat(4, 8, 9))   # Output: [12, 1]
# print(eat(1, 10, 10)) # Output: [11, 0]
# print(eat(2, 11, 5))  # Output: [7, 0]