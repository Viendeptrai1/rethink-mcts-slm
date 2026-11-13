def find_pattern(n, m, filenames, indices_to_delete):
    # Extract the filenames to be deleted based on indices
    files_to_delete = [filenames[i - 1] for i in indices_to_delete]

    # If there is only one file to delete, it's the pattern itself
    if m == 1:
        return "Yes", files_to_delete[0]

    # Initialize the pattern with the first file to delete
    pattern = list(files_to_delete[0])

    # Compare each character in the pattern with the other files to delete
    for file in files_to_delete[1:]:
        for i in range(len(pattern)):
            if pattern[i] != '?' and pattern[i] != file[i]:
                pattern[i] = '?'

    # Ensure that the pattern has the same length as the files
    pattern = ''.join(pattern)

    # Check if the constructed pattern matches all the files to delete and none of the others
    all_files = set(filenames)
    deleted_files = set(files_to_delete)
    remaining_files = all_files - deleted_files

    for file in deleted_files:
        if not matches_pattern(file, pattern):
            return "No", ""

    for file in remaining_files:
        if matches_pattern(file, pattern):
            return "No", ""

    return "Yes", pattern

def matches_pattern(filename, pattern):
    if len(filename) != len(pattern):
        return False
    for i in range(len(filename)):
        if pattern[i] != '?' and filename[i] != pattern[i]:
            return False
    return True

# Read input
import sys
input = sys.stdin.read
data = input().splitlines()

n, m = map(int, data[0].split())
filenames = data[1:n+1]
indices_to_delete = list(map(int, data[n+1].split()))

# Find pattern
result, pattern = find_pattern(n, m, filenames, indices_to_delete)

# Print output
print(result)
if result == "Yes":
    print(pattern)