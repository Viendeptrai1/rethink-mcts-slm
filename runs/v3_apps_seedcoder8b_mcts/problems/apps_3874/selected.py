def find_deletion_pattern(n, m, filenames, indices_to_delete):
    files_to_delete = [filenames[i - 1] for i in indices_to_delete]
    
    def matches(pattern, filename):
        if len(pattern) != len(filename):
            return False
        return all(p == '?' or p == f for p, f in zip(pattern, filename))
    
    def find_pattern(files):
        if not files:
            return None
        file_length = len(files[0])
        for length in range(file_length, file_length + 1):
            for start in range(file_length - length + 1):
                pattern = ['?'] * length
                for file in files:
                    if len(file) != length:
                        continue
                    for i in range(length):
                        if pattern[i] == '?':
                            pattern[i] = file[i]
                        elif pattern[i] != file[i]:
                            pattern[i] = '?'
                            break
                if all(matches(pattern, file) for file in files):
                    return ''.join(pattern)
        return None
    
    pattern = find_pattern(files_to_delete)
    if pattern:
        print("Yes")
        print(pattern)
    else:
        print("No")

# Example usage:
import sys
input = sys.stdin.read
data = input().splitlines()
n, m = map(int, data[0].split())
filenames = data[1:n+1]
indices_to_delete = list(map(int, data[n+1].split()))
find_deletion_pattern(n, m, filenames, indices_to_delete)