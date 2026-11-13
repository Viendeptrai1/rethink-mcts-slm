import re

def fruit_distribution(s, n):
    match = re.search(r'(\d+) apples and (\d+) oranges', s)
    if match:
        apples = int(match.group(1))
        oranges = int(match.group(2))
        mangoes = n - apples - oranges
        return mangoes
    else:
        raise ValueError("Invalid input format")