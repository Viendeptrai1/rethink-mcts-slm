def min_replacements_to_lucky(ticket):
    first_half_sum = sum(int(ticket[i]) for i in range(3))
    second_half_sum = sum(int(ticket[i]) for i in range(3, 6))
    diff = abs(first_half_sum - second_half_sum)
    return diff // 9 + (diff % 9 != 0)

# Example usage:
ticket = input().strip()
print(min_replacements_to_lucky(ticket))