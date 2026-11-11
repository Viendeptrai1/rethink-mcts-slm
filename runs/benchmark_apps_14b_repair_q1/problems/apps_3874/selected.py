import sys

def find_pattern(n, m, filenames, indices_to_delete):
    # Convert indices to zero-based for easier manipulation
    indices_to_delete = [x - 1 for x in indices_to_delete]
    
    # Initialize the pattern with '?'
    pattern = ['?'] * len(filenames[0])
    
    # Iterate over each character position in the filenames
    for i in range(len(filenames[0])):
        # Get the set of characters at the current position for the files to be deleted
        chars_to_match = {filenames[j][i] for j in indices_to_delete}
        
        # If there's more than one unique character at this position, we can't match exactly
        if len(chars_to_match) > 1:
            continue
        
        # Set the pattern character to the only matching character found
        pattern[i] = chars_to_match.pop()
    
    # Check if the pattern matches exactly the files to be deleted
    def matches(filename, pattern):
        if len(filename) != len(pattern):
            return False
        for f_char, p_char in zip(filename, pattern):
            if p_char != '?' and f_char != p_char:
                return False
        return True
    
    # Verify the pattern
    if all(matches(filenames[j], pattern) for j in indices_to_delete) and \
       not any(matches(filenames[j], pattern) for j in range(n) if j not in indices_to_delete):
        return "Yes", ''.join(pattern)
    else:
        return "No", ""

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    filenames = data[2:2+n]
    indices_to_delete = list(map(int, data[2+n:2+n+m]))
    
    result, pattern = find_pattern(n, m, filenames, indices_to_delete)
    print(result)
    if result == "Yes":
        print(pattern)

if __name__ == "__main__":
    main()