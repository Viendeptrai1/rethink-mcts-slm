def fruit_distribution(s, n):
    # Extract numbers from the string
    parts = s.split()
    apples = int(parts[0])
    oranges = int(parts[3])
    
    # Calculate the number of mangoes
    mangoes = n - apples - oranges
    return mangoes

# Example usage:
# print(fruit_distribution("5 apples and 6 oranges", 19))  # Output: 8
# print(fruit_distribution("0 apples and 1 oranges", 3))   # Output: 2
# print(fruit_distribution("2 apples and 3 oranges", 100)) # Output: 95
# print(fruit_distribution("100 apples and 1 oranges", 120)) # Output: 19