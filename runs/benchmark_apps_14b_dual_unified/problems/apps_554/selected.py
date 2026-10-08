import sys
from itertools import combinations

def max_happiness(n, m, a, subarrays):
    max_happy = float('-inf')
    
    # Iterate over all possible subsets of subarrays
    for r in range(1, m + 1):
        for subset in combinations(subarrays, r):
            happiness = [0] * n
            for l, r in subset:
                for i in range(l - 1, r):
                    happiness[i] += a[i]
            max_happy = max(max_happy, sum(happiness))
    
    return max_happy

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    m = int(data[index + 1])
    index += 2
    
    a = list(map(int, data[index:index + n]))
    index += n
    
    subarrays = []
    for _ in range(m):
        l = int(data[index])
        r = int(data[index + 1])
        subarrays.append((l, r))
        index += 2
    
    result = max_happiness(n, m, a, subarrays)
    print(result)