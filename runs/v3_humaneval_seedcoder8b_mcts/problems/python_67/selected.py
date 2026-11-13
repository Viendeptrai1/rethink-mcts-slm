import re

def fruit_distribution(s, n):
    # Extract numbers from the string using regular expressions
    numbers = re.findall(r'\d+', s)
    # Convert the extracted numbers to integers
    apples = int(numbers[0])
    oranges = int(numbers[1])
    # Calculate the number of mangoes
    mangoes = n - apples - oranges
    return mangoes