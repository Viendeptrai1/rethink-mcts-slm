import sys
from collections import defaultdict

def find_index_to_remove(n, b):
    if n == 2:
        return 1
    
    freq = defaultdict(int)
    for i in range(n):
        for j in range(i + 1, n):
            if b[i] != b[j]:
                d = (b[j] - b[i]) / (j - i)
                if d.is_integer():
                    d = int(d)
                    count = 0
                    for k in range(n):
                        if k != i and k != j:
                            if b[k] == b[i] + d * (k - i):
                                count += 1
                    if count + 2 == n:
                        return i + 1
    
    return -1

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    b = list(map(int, data[1:]))
    
    result = find_index_to_remove(n, b)
    print(result)

if __name__ == "__main__":
    main()