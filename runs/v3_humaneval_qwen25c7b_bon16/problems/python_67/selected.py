import re

def fruit_distribution(s, n):
    # Use regular expressions to find numbers in the string
    numbers = re.findall(r'\d+', s)
    # Convert found numbers to integers and sum them
    count_apples_oranges = sum(map(int, numbers))
    # Subtract the sum of apples and oranges from the total number of fruits
    return n - count_apples_oranges