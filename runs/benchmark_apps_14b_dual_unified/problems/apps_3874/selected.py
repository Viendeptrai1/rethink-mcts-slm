import sys

def find_pattern(n, m, filenames, indices):
    # Extract the filenames to be deleted
    to_delete = [filenames[i-1] for i in indices]
    
    # Find the minimum length among the filenames to be deleted
    min_len = min(len(name) for name in to_delete)
    
    # Initialize the pattern with the first filename
    pattern = list(to_delete[0][:min_len])
    
    # Compare with other filenames to be deleted and adjust the pattern
    for name in to_delete[1:]:
        for i in range(min_len):
            if pattern[i] != name[i]:
                pattern[i] = '?'
    
    # Check if the pattern matches only the intended filenames
    pattern_str = ''.join(pattern)
    matches = [name for name in filenames if len(name) == min_len and all(a == b or b == '?' for a, b in zip(name, pattern))]
    
    if len(matches) == m:
        return "Yes", pattern_str
    else:
        return "No", ""

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    filenames = data[2:2+n]
    indices = list(map(int, data[2+n:]))
    
    result, pattern = find_pattern(n, m, filenames, indices)
    print(result)
    if result == "Yes":
        print(pattern)

if __name__ == "__main__":
    main()