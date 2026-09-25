def get_max_triples(n):
    # Create the array a where a[i] = i * i - i + 1
    a = [i * i - i + 1 for i in range(1, n + 1)]
    
    # Count the number of elements in a that have remainders 0, 1, and 2 when divided by 3
    count_mod_0 = count_mod_1 = count_mod_2 = 0
    
    for num in a:
        if num % 3 == 0:
            count_mod_0 += 1
        elif num % 3 == 1:
            count_mod_1 += 1
        else:
            count_mod_2 += 1
    
    # Calculate the number of valid triples
    # (0, 0, 0), (1, 1, 1), (2, 2, 2)
    triples_0 = count_mod_0 * (count_mod_0 - 1) * (count_mod_0 - 2) // 6
    triples_1 = count_mod_1 * (count_mod_1 - 1) * (count_mod_1 - 2) // 6
    triples_2 = count_mod_2 * (count_mod_2 - 1) * (count_mod_2 - 2) // 6
    
    # (0, 1, 2)
    triples_012 = count_mod_0 * count_mod_1 * count_mod_2
    
    # Total number of valid triples
    total_triples = triples_0 + triples_1 + triples_2 + triples_012
    
    return total_triples

# Example usage
print(get_max_triples(5))  # Output: 1