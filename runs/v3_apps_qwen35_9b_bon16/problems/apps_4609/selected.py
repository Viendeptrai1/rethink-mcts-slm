import sys
from collections import Counter

def solve():
    input = sys.stdin.read
    data = input().split()
    if not data:
        return
    
    n = int(data[0])
    a = data[1:]
    
    counter = Counter()
    for x in a:
        counter[x] += 1
    
    result = 0
    for count in counter.values():
        if count % 2 == 1:
            result += 1
    
    print(result)

if __name__ == "__main__":
    solve()