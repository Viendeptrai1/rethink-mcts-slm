def get_max_triples(n):
    # Step 1: Calculate the values of the array a
    a = [i * i - i + 1 for i in range(1, n + 1)]
    
    # Step 2: Count the number of elements in a that have remainders 0, 1, and 2 when divided by 3
    count_mod_0 = count_mod_1 = count_mod_2 = 0
    for value in a:
        if value % 3 == 0:
            count_mod_0 += 1
        elif value % 3 == 1:
            count_mod_1 += 1
        else:
            count_mod_2 += 1
    
    # Step 3: Calculate the number of valid triples
    # Valid triples can be formed in the following ways:
    # (0, 0, 0), (1, 1, 1), (2, 2, 2), (0, 1, 2)
    triples_count = (
        (count_mod_0 * (count_mod_0 - 1) * (count_mod_0 - 2)) // 6 +  # (0, 0, 0)
        (count_mod_1 * (count_mod_1 - 1) * (count_mod_1 - 2)) // 6 +  # (1, 1, 1)
        (count_mod_2 * (count_mod_2 - 1) * (count_mod_2 - 2)) // 6 +  # (2, 2, 2)
        count_mod_0 * count_mod_1 * count_mod_2  # (0, 1, 2)
    )
    
    return triples_count

# Example usage:
# print(get_max_triples(5))  # Output: 1