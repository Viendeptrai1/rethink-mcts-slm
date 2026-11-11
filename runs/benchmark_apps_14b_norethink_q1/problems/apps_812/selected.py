import sys
from collections import defaultdict

def find_index_to_remove(n, b):
    def is_arithmetic(seq):
        if len(seq) <= 1:
            return True
        seq.sort()
        diff = seq[1] - seq[0]
        for i in range(2, len(seq)):
            if seq[i] - seq[i - 1] != diff:
                return False
        return True

    for j in range(n):
        remaining = b[:j] + b[j+1:]
        if is_arithmetic(remaining):
            return j + 1
    return -1

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    b = list(map(int, data[1:]))
    
    result = find_index_to_remove(n, b)
    print(result)