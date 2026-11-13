import re

def fruit_distribution(s, n):
    apples_match = re.search(r'(\d+)\s*apples', s)
    oranges_match = re.search(r'(\d+)\s*oranges', s)
    
    apples = int(apples_match.group(1)) if apples_match else 0
    oranges = int(oranges_match.group(1)) if oranges_match else 0
    
    return n - apples - oranges