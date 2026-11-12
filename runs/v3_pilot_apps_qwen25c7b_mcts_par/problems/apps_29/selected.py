def min_replacements_to_lucky(ticket):
    first_half_sum = int(ticket[0]) + int(ticket[1]) + int(ticket[2])
    second_half_sum = int(ticket[3]) + int(ticket[4]) + int(ticket[5])
    
    difference = abs(first_half_sum - second_half_sum)
    
    # Each replacement can change the sum by at most 9 (e.g., changing '0' to '9')
    min_replacements = difference // 9
    
    # If there's a remainder, we need an additional replacement
    if difference % 9 != 0:
        min_replacements += 1
    
    return min_replacements

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    print(min_replacements_to_lucky(input))