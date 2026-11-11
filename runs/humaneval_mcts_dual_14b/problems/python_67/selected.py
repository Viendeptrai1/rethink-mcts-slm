import re

def fruit_distribution(s, n):
    # Use regular expressions to find all numbers in the string
    numbers = re.findall(r'\d+', s)
    # Convert the found numbers to integers
    apples = int(numbers[0])
    oranges = int(numbers[1])
    # Calculate the number of mangoes
    mangoes = n - apples - oranges
    return mangoes