def min_replacements_to_lucky(ticket):
    first_half_sum = sum(int(digit) for digit in ticket[:3])
    second_half_sum = sum(int(digit) for digit in ticket[3:])
    
    if first_half_sum == second_half_sum:
        return 0
    
    replacements = 0
    target_diff = abs(first_half_sum - second_half_sum)
    
    for i in range(3):
        if int(ticket[i]) != int(ticket[3 + i]):
            replacements += 1
            if replacements >= target_diff:
                break
    
    return replacements

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read().strip()
    print(min_replacements_to_lucky(input))