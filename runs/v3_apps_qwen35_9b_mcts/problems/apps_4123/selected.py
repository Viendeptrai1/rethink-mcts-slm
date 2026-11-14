import sys
from collections import Counter

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    s = input_data[1]
    
    two_grams = []
    for i in range(n - 1):
        two_grams.append(s[i:i+2])
    
    counts = Counter(two_grams)
    max_count = -1
    result = ""
    
    for gram in sorted(counts.keys()):
        if counts[gram] > max_count:
            max_count = counts[gram]
            result = gram
    
    print(result)

if __name__ == "__main__":
    solve()