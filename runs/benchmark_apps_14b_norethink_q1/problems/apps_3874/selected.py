import sys

def find_deletion_pattern(n, m, filenames, indices_to_delete):
    # Extract the filenames to be deleted
    files_to_delete = [filenames[i-1] for i in indices_to_delete]
    
    # Check if all files to be deleted have the same length
    if len(set(len(f) for f in files_to_delete)) != 1:
        return "No"
    
    # Get the length of the filenames
    length = len(files_to_delete[0])
    
    # Create the pattern
    pattern = []
    for i in range(length):
        chars = {f[i] for f in files_to_delete}
        if len(chars) == 1:
            pattern.append(next(iter(chars)))
        else:
            pattern.append('?')
    
    return "Yes", "".join(pattern)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    filenames = data[2:2+n]
    indices_to_delete = list(map(int, data[2+n:2+n+m]))
    
    result = find_deletion_pattern(n, m, filenames, indices_to_delete)
    if result == "No":
        print("No")
    else:
        print("Yes")
        print(result[1])

if __name__ == "__main__":
    main()