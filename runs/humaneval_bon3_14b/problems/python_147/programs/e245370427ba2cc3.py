def get_max_triples(n):
    # Create the array a according to the given formula
    a = [i * i - i + 1 for i in range(1, n + 1)]
    
    # Count the occurrences of each remainder when elements of a are divided by 3
    count_mod_0 = count_mod_1 = count_mod_2 = 0
    
    for num in a:
        if num % 3 == 0:
            count_mod_0 += 1
        elif num % 3 == 1:
            count_mod_1 += 1
        else:
            count_mod_2 += 1
    
    # Calculate the number of valid triples
    # Case 1: All three numbers have the same remainder when divided by 3
    triples_same_remainder = (
        (count_mod_0 * (count_mod_0 - 1) * (count_mod_0 - 2)) // 6 +
        (count_mod_1 * (count_mod_1 - 1) * (count_mod_1 - 2)) // 6 +
        (count_mod_2 * (count_mod_2 - 1) * (count_mod_2 - 2)) // 6
    )
    
    # Case 2: All three numbers have different remainders when divided by 3
    triples_different_remainder = count_mod_0 * count_mod_1 * count_mod_2
    
    # Total number of valid triples
    total_triples = triples_same_remainder + triples_different_remainder
    
    return total_triples

# Example usage:
# print(get_max_triples(5))  # Output: 1