def find_typos(dictionary):
    # Create a set for faster lookup
    dict_set = set(dictionary)
    
    typos = []
    
    # Iterate through each word in the dictionary
    for word in dictionary:
        # Generate all possible words by deleting one character
        for i in range(len(word)):
            candidate = word[:i] + word[i+1:]
            # Check if the candidate word exists in the dictionary
            if candidate in dict_set:
                typos.append(word)
                break
    
    return typos

# Read input
import sys
input = sys.stdin.read
data = input().split()

# Number of words in the dictionary
n = int(data[0])

# Dictionary of words
dictionary = data[1:n+1]

# Find typos
typos = find_typos(dictionary)

# Output typos or "NO TYPOS" if there are none
if typos:
    print(*typos, sep='\n')
else:
    print("NO TYPOS")