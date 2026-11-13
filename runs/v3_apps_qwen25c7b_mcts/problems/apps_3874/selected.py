import sys

def find_pattern(n, m, filenames, to_delete):
    def matches(pattern, filename):
        return len(pattern) == len(filename) and all(p == f or p == '?' for p, f in zip(pattern, filename))

    for i in range(1 << len(filenames[0])):
        pattern = ''.join('?' if (i >> j) & 1 else c for j, c in enumerate(filenames[0]))
        count = sum(matches(pattern, filenames[j]) for j in range(n))
        if count == m:
            print("Yes")
            print(pattern)
            return
    print("No")

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    filenames = [data[i + 2] for i in range(n)]
    to_delete = list(map(int, data[n + 2:n + 2 + m]))
    
    find_pattern(n, m, filenames, to_delete)