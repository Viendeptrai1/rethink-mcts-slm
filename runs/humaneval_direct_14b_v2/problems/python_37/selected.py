def sort_even(l: list):
    even_indices = [i for i in range(len(l)) if i % 2 == 0]
    even_values = [l[i] for i in even_indices]
    even_values.sort()
    
    l_prime = l[:]
    for idx, value in zip(even_indices, even_values):
        l_prime[idx] = value
    
    return l_prime