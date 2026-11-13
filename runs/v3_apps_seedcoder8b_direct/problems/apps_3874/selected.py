def find_deletion_pattern():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    n, m = map(int, data[0].split())
    filenames = data[1:n+1]
    indices_to_delete = list(map(int, data[n+1].split()))
    
    files_to_delete = [filenames[i-1] for i in indices_to_delete]
    
    if not files_to_delete:
        print("No")
        return
    
    # Function to check if two strings match the pattern
    def match_pattern(pattern, filename):
        if len(pattern) != len(filename):
            return False
        for p_char, f_char in zip(pattern, filename):
            if p_char != '?' and p_char != f_char:
                return False
        return True
    
    # Try to find a pattern that matches all files to be deleted
    pattern_length = len(files_to_delete[0])
    pattern = ['?'] * pattern_length
    
    for filename in files_to_delete:
        if len(filename) != pattern_length:
            print("No")
            return
        for i in range(pattern_length):
            if pattern[i] == '?':
                pattern[i] = filename[i]
            elif pattern[i] != filename[i]:
                pattern[i] = '?'
    
    # Verify the pattern matches all files to be deleted and no others
    for filename in filenames:
        if filename in files_to_delete and not match_pattern(pattern, filename):
            print("No")
            return
        if filename not in files_to_delete and match_pattern(pattern, filename):
            print("No")
            return
    
    print("Yes")
    print(''.join(pattern))