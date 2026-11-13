import sys
from collections import Counter

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    s = data[1]
    
    two_grams = []
    for i in range(n - 1):
        two_grams.append(s[i:i+2])
    
    counts = Counter(two_grams)
    max_count = 0
    result = ""
    
    for gram, count in counts.items():
        if count > max_count:
            max_count = count
            result = gram
    
    print(result)

if __name__ == "__main__":
    solve()