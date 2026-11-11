def get_max_triples(n):
    # Initialize counts for remainders 0, 1, and 2
    count_0 = count_1 = count_2 = 0
    
    # Calculate the values of the array a and count their remainders
    for i in range(1, n + 1):
        value = i * i - i + 1
        remainder = value % 3
        if remainder == 0:
            count_0 += 1
        elif remainder == 1:
            count_1 += 1
        else:
            count_2 += 1
    
    # Calculate the number of valid triples
    # Case 1: All three numbers have remainder 0
    triples_0 = count_0 * (count_0 - 1) * (count_0 - 2) // 6
    
    # Case 2: All three numbers have remainder 1
    triples_1 = count_1 * (count_1 - 1) * (count_1 - 2) // 6
    
    # Case 3: All three numbers have remainder 2
    triples_2 = count_2 * (count_2 - 1) * (count_2 - 2) // 6
    
    # Case 4: One number from each remainder category
    triples_mixed = count_0 * count_1 * count_2
    
    # Total number of valid triples
    total_triples = triples_0 + triples_1 + triples_2 + triples_mixed
    
    return total_triples