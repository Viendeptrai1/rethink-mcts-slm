import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    n = int(next(iterator))
    m = int(next(iterator))

    filenames = []
    for _ in range(n):
        filenames.append(next(iterator))

    target_indices = []
    for _ in range(m):
        target_indices.append(int(next(iterator)) - 1)

    target_files = [filenames[i] for i in target_indices]

    if m == 1:
        print("Yes")
        print(target_files[0])
        return

    # Check if all target files have the same length
    length = len(target_files[0])
    for f in target_files:
        if len(f) != length:
            print("No")
            return

    # Construct the pattern based on the first target file
    pattern_chars = list(target_files[0])
    for i in range(1, len(target_files)):
        other = target_files[i]
        for j in range(length):
            if pattern_chars[j] != '?' and pattern_chars[j] != other[j]:
                pattern_chars[j] = '?'

    pattern = "".join(pattern_chars)

    # Verify the pattern matches exactly the target files
    for f in target_files:
        if len(f) != length:
            print("No")
            return
        match = True
        for j in range(length):
            p_char = pattern[j]
            f_char = f[j]
            if p_char != '?' and p_char != f_char:
                match = False
                break
        if not match:
            print("No")
            return

    # Verify the pattern does not match any non-target files
    for i in range(n):
        if i in target_indices:
            continue
        f = filenames[i]
        if len(f) != length:
            continue
        match = True
        for j in range(length):
            p_char = pattern[j]
            f_char = f[j]
            if p_char != '?' and p_char != f_char:
                match = False
                break
        if match:
            print("No")
            return

    print("Yes")
    print(pattern)

if __name__ == "__main__":
    solve()