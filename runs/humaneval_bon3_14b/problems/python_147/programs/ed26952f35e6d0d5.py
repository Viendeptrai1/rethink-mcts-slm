def get_max_triples(n):
    # Create the array a where a[i] = i * i - i + 1
    a = [i * i - i + 1 for i in range(1, n + 1)]
    
    # Count the remainders when elements of a are divided by 3
    count_mod_0 = 0
    count_mod_1 = 0
    count_mod_2 = 0
    
    for num in a:
        if num % 3 == 0:
            count_mod_0 += 1
        elif num % 3 == 1:
            count_mod_1 += 1
        else:
            count_mod_2 += 1
    
    # Calculate the number of valid triples
    # (0, 0, 0), (1, 1, 1), (2, 2, 2)
    triples = (
        count_mod_0 * (count_mod_0 - 1) * (count_mod_0 - 2) // 6 +
        count_mod_1 * (count_mod_1 - 1) * (count_mod_1 - 2) // 6 +
        count_mod_2 * (count_mod_2 - 1) * (count_mod_2 - 2) // 6
    )
    
    # (0, 1, 2)
    triples += count_mod_0 * count_mod_1 * count_mod_2
    
    return triples

# Example usage
print(get_max_triples(5))  # Output: 1