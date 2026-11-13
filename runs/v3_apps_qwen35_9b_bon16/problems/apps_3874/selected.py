import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    n = int(next(iterator))
    m = int(next(iterator))
    
    files = []
    for _ in range(n):
        files.append(next(iterator))
    
    to_delete_indices = []
    for _ in range(m):
        to_delete_indices.append(int(next(iterator)) - 1)
    
    to_delete_set = set(to_delete_indices)
    
    if m == 0:
        print("Yes")
        print("")
        return

    # Check if all files to be deleted have the same length
    target_len = len(files[to_delete_indices[0]])
    for idx in to_delete_indices:
        if len(files[idx]) != target_len:
            print("No")
            return

    # Build the pattern based on files to be deleted
    # For each position, if all target files have the same char, use it.
    # Otherwise, use '?'.
    pattern_chars = []
    for i in range(target_len):
        chars_at_i = set()
        for idx in to_delete_indices:
            chars_at_i.add(files[idx][i])
        
        if len(chars_at_i) == 1:
            pattern_chars.append(list(chars_at_i)[0])
        else:
            pattern_chars.append('?')
    
    candidate_pattern = "".join(pattern_chars)
    
    # Verify the pattern matches all files to be deleted
    for idx in to_delete_indices:
        if not match_pattern(candidate_pattern, files[idx]):
            print("No")
            return
    
    # Verify the pattern does NOT match any file NOT to be deleted
    for i in range(n):
        if i in to_delete_set:
            continue
        if match_pattern(candidate_pattern, files[i]):
            print("No")
            return
    
    print("Yes")
    print(candidate_pattern)

def match_pattern(pattern, filename):
    if len(pattern) != len(filename):
        return False
    for p_char, f_char in zip(pattern, filename):
        if p_char != '?' and p_char != f_char:
            return False
    return True

if __name__ == "__main__":
    solve()