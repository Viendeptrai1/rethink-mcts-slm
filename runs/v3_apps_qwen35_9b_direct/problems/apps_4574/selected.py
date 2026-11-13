import sys
from collections import Counter

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = list(map(int, input_data[1:]))
    
    count = Counter(a)
    pairs = []
    
    for length, freq in count.items():
        if freq >= 2:
            pairs.append(length)
            if freq >= 4:
                pairs.append(length)
    
    pairs.sort(reverse=True)
    
    if len(pairs) < 2:
        print(0)
        return
    
    max_area = pairs[0] * pairs[1]
    print(max_area)

if __name__ == "__main__":
    solve()