import sys
from itertools import combinations

def min_cost_to_form_set(n, k, s):
    subsequences = set()
    for i in range(1, n + 1):
        for comb in combinations(s, i):
            subsequences.add(''.join(comb))
    
    subsequences = sorted(subsequences, key=lambda x: len(x))
    
    if len(subsequences) < k:
        return -1
    
    total_cost = 0
    for i in range(k):
        total_cost += n - len(subsequences[i])
    
    return total_cost

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    s = data[2]
    
    result = min_cost_to_form_set(n, k, s)
    print(result)

if __name__ == "__main__":
    main()