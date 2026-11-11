import sys
from collections import defaultdict
from math import factorial

MOD = 10**9 + 9

def count_entirely_unsorted_sequences(n, a):
    # Step 1: Identify sorted positions
    sorted_positions = set()
    stack = []
    
    for i in range(n):
        while stack and a[stack[-1]] <= a[i]:
            sorted_positions.add(stack.pop())
        stack.append(i)
    
    for i in range(n-1, -1, -1):
        while stack and a[stack[-1]] <= a[i]:
            sorted_positions.add(stack.pop())
        stack.append(i)
    
    # Step 2: Calculate the number of unsorted positions
    unsorted_count = n - len(sorted_positions)
    
    # Step 3: Count the frequency of each element in the unsorted positions
    freq = defaultdict(int)
    for i in range(n):
        if i not in sorted_positions:
            freq[a[i]] += 1
    
    # Step 4: Calculate the number of permutations of the unsorted elements
    total_permutations = factorial(unsorted_count) % MOD
    for count in freq.values():
        total_permutations *= pow(factorial(count), MOD-2, MOD)
        total_permutations %= MOD
    
    return total_permutations

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    result = count_entirely_unsorted_sequences(n, a)
    print(result)

if __name__ == "__main__":
    main()