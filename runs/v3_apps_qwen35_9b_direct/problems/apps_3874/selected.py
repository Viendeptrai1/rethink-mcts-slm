import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        n = int(next(iterator))
        m = int(next(iterator))
    except StopIteration:
        return

    filenames = []
    for _ in range(n):
        filenames.append(next(iterator))

    indices_to_delete = []
    for _ in range(m):
        indices_to_delete.append(int(next(iterator)) - 1)

    # Check if all files to be deleted have the same length
    target_len = len(filenames[indices_to_delete[0]])
    for idx in indices_to_delete:
        if len(filenames[idx]) != target_len:
            print("No")
            return

    # Build the pattern based on files to be deleted
    pattern_chars = []
    for i in range(target_len):
        char = filenames[indices_to_delete[0]][i]
        # Check if this character is consistent across all files to be deleted
        consistent = True
        for idx in indices_to_delete:
            if filenames[idx][i] != char:
                consistent = False
                break
        if consistent:
            pattern_chars.append(char)
        else:
            pattern_chars.append('?')

    pattern = "".join(pattern_chars)

    # Verify the pattern against all files
    # 1. All files to be deleted must match
    for idx in indices_to_delete:
        if not match(pattern, filenames[idx]):
            print("No")
            return

    # 2. All other files must NOT match
    for i in range(n):
        if i not in indices_to_delete:
            if match(pattern, filenames[i]):
                print("No")
                return

    print("Yes")
    print(pattern)

def match(pattern, filename):
    if len(pattern) != len(filename):
        return False
    for p_char, f_char in zip(pattern, filename):
        if p_char != '?' and p_char != f_char:
            return False
    return True

if __name__ == "__main__":
    solve()