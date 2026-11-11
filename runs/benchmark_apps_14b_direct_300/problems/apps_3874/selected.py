def find_pattern(n, m, filenames, indices):
    # Convert indices to zero-based for easier manipulation
    indices = [i - 1 for i in indices]
    
    # Initialize the pattern with '?'
    pattern = ['?'] * len(filenames[0])
    
    # Iterate over each character position
    for pos in range(len(filenames[0])):
        # Get the set of characters at this position for files to be deleted
        chars_to_delete = set(filenames[i][pos] for i in indices)
        
        # Get the set of characters at this position for all files
        all_chars = set(filename[pos] for filename in filenames)
        
        # If there's a character in all files that's not in the files to be deleted, we can't match
        if all_chars - chars_to_delete:
            return "No"
        
        # If all characters in the files to be deleted are the same, fix the pattern
        if len(chars_to_delete) == 1:
            pattern[pos] = next(iter(chars_to_delete))
    
    return "Yes\n" + "".join(pattern)

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
filenames = data[2:2+n]
indices = list(map(int, data[2+n:]))

# Find and print the pattern
result = find_pattern(n, m, filenames, indices)
print(result)