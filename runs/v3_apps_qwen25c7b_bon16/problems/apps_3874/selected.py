def find_deletion_pattern(filenames, delete_indices):
    m = len(delete_indices)
    n = len(filenames)
    
    # Create a list of booleans indicating whether a file should be deleted
    delete_flags = [False] * n
    for index in delete_indices:
        delete_flags[index - 1] = True
    
    # Initialize the pattern with the first filename
    pattern = filenames[delete_indices[0] - 1]
    
    # Try to construct a pattern that matches all delete files and none of the others
    for i in range(1, m):
        current_pattern = ""
        for j in range(len(pattern)):
            if pattern[j] == filenames[delete_indices[i] - 1][j]:
                current_pattern += pattern[j]
            elif delete_flags[delete_indices[i] - 1]:
                current_pattern += '?'
            else:
                return "No"
        pattern = current_pattern
    
    # Check if the constructed pattern matches all delete files and none of the others
    for i in range(m):
        if not pattern_match(filenames[delete_indices[i] - 1], pattern):
            return "No"
    
    for i in range(n):
        if delete_flags[i] != pattern_match(filenames[i], pattern):
            return "No"
    
    return "Yes\n" + pattern

def pattern_match(filename, pattern):
    if len(filename) != len(pattern):
        return False
    for i in range(len(pattern)):
        if pattern[i] != filename[i] and pattern[i] != '?':
            return False
    return True

# Example usage
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    filenames = data[2:2+n]
    delete_indices = list(map(int, data[2+n:]))
    
    result = find_deletion_pattern(filenames, delete_indices)
    print(result)