def get_max_triples(n):
    a = [i * i - i + 1 for i in range(1, n + 1)]
    count_mod_0 = count_mod_1 = count_mod_2 = 0
    
    for num in a:
        if num % 3 == 0:
            count_mod_0 += 1
        elif num % 3 == 1:
            count_mod_1 += 1
        else:
            count_mod_2 += 1
    
    # Calculate the number of valid triples
    triples = (
        count_mod_0 * (count_mod_0 - 1) * (count_mod_0 - 2) // 6 +
        count_mod_1 * (count_mod_1 - 1) * (count_mod_1 - 2) // 6 +
        count_mod_2 * (count_mod_2 - 1) * (count_mod_2 - 2) // 6 +
        count_mod_0 * count_mod_1 * count_mod_2
    )
    
    return triples