def find_deletion_pattern(n, m, filenames, to_delete):
    # Extract the filenames to be deleted
    delete_files = [filenames[i-1] for i in to_delete]
    
    # Find the common prefix among the files to be deleted
    prefix = ""
    for i in range(min(len(delete_files[0]), len(delete_files[1]))):
        if delete_files[0][i] == delete_files[1][i]:
            prefix += delete_files[0][i]
        else:
            break
    
    # Check if the common prefix can be extended to match all files to be deleted
    for file in delete_files[2:]:
        if not file.startswith(prefix):
            return "No"
    
    # Create the deletion pattern
    pattern = prefix
    for char in delete_files[0][len(prefix):]:
        if char != delete_files[1][len(prefix):][0]:
            pattern += "?"
        else:
            pattern += char
    
    # Check if the pattern matches all files to be deleted
    for file in delete_files:
        if not file.startswith(pattern):
            return "No"
    
    return "Yes\n" + pattern

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
m = int(data[1])
filenames = data[2:n+2]
to_delete = list(map(int, data[n+2:]))

# Output result
result = find_deletion_pattern(n, m, filenames, to_delete)
print(result)