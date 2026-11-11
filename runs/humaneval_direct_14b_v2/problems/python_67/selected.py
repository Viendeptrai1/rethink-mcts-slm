def fruit_distribution(s, n):
    # Extract numbers from the string
    words = s.split()
    apples = int(words[0])
    oranges = int(words[3])
    
    # Calculate the number of mangoes
    mangoes = n - apples - oranges
    return mangoes