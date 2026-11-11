import sys
from collections import Counter

def main():
    import sys
    import collections
    
    def read_ints():
        return list(map(int, sys.stdin.readline().split()))
    
    n, m, p = read_ints()
    a = read_ints()
    b = read_ints()
    
    b_counter = Counter(b)
    valid_positions = []
    
    for q in range(1, n - (m - 1) * p + 1):
        subsequence = [a[q - 1 + i * p] for i in range(m)]
        subseq_counter = Counter(subsequence)
        if subseq_counter == b_counter:
            valid_positions.append(q)
    
    print(len(valid_positions))
    print(*valid_positions)

if __name__ == "__main__":
    main()