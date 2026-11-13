import sys
from collections import defaultdict

def rev(n):
    return int(str(n)[::-1])

def calculate_appearances(limit):
    appearances = defaultdict(int)
    row = 1
    while True:
        current_value = row
        while current_value <= limit:
            appearances[current_value] += 1
            current_value += rev(current_value)
        if row > limit:
            break
        row += 1
    return appearances

def prefix_sums(appearances):
    sorted_keys = sorted(appearances.keys())
    prefix = 0
    prefix_sums = {}
    for key in sorted_keys:
        prefix += appearances[key]
        prefix_sums[key] = prefix
    return prefix_sums

def count_appearances_in_range(prefix_sums, A, B):
    if A not in prefix_sums:
        A = min(k for k in prefix_sums.keys() if k >= A)
    if B not in prefix_sums:
        B = max(k for k in prefix_sums.keys() if k <= B)
    return prefix_sums[B] - prefix_sums[A] + appearances[A]

def main():
    input = sys.stdin.read
    data = input().split()
    
    Q = int(data[0])
    queries = [(int(data[i]), int(data[i+1])) for i in range(1, 2*Q, 2)]
    
    global appearances
    appearances = calculate_appearances(10**10)
    prefix_sums_dict = prefix_sums(appearances)
    
    results = []
    for A, B in queries:
        result = count_appearances_in_range(prefix_sums_dict, A, B)
        results.append(result)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()