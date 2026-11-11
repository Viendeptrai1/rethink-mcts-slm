import sys
from collections import defaultdict

MOD = 998244353

def count_good_permutations(n, pairs):
    def is_sorted(arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
    
    first_elements = [pair[0] for pair in pairs]
    second_elements = [pair[1] for pair in pairs]
    
    if is_sorted(first_elements) or is_sorted(second_elements):
        return 0
    
    # Count the frequency of each element in first and second elements
    first_count = defaultdict(int)
    second_count = defaultdict(int)
    
    for a, b in pairs:
        first_count[a] += 1
        second_count[b] += 1
    
    # Calculate the number of permutations that keep the sequence bad
    bad_permutations = 1
    
    for count in first_count.values():
        bad_permutations = bad_permutations * factorial(count) % MOD
    
    for count in second_count.values():
        bad_permutations = bad_permutations * factorial(count) % MOD
    
    # Total permutations
    total_permutations = factorial(n)
    
    # Good permutations = Total permutations - Bad permutations
    good_permutations = (total_permutations - bad_permutations) % MOD
    
    return good_permutations

def factorial(x):
    result = 1
    for i in range(2, x + 1):
        result = result * i % MOD
    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    pairs = []
    index = 1
    for _ in range(n):
        a = int(data[index])
        b = int(data[index + 1])
        pairs.append((a, b))
        index += 2
    
    result = count_good_permutations(n, pairs)
    print(result)

if __name__ == "__main__":
    main()