import sys
from collections import defaultdict

def rev_number(n):
    return int(str(n)[::-1])

def calculate_appearances(max_value):
    appearances = defaultdict(int)
    
    def calculate_value(i, j):
        if j == 1:
            return i
        left_value = calculate_value(i, j - 1)
        return left_value + rev_number(left_value)
    
    row, col = 1, 1
    while True:
        value = calculate_value(row, col)
        if value > max_value:
            break
        appearances[value] += 1
        col += 1
        if col == 1:
            row += 1
    
    # Accumulate the appearances
    sorted_keys = sorted(appearances.keys())
    for i in range(1, len(sorted_keys)):
        appearances[sorted_keys[i]] += appearances[sorted_keys[i - 1]]
    
    return appearances

def query_appearances(queries, appearances):
    result = []
    for a, b in queries:
        if a in appearances and b in appearances:
            result.append(appearances[b] - appearances[a - 1])
        elif a in appearances:
            result.append(appearances[b])
        elif b in appearances:
            result.append(appearances[b] - appearances[a - 1])
        else:
            result.append(0)
    return result

def main():
    input = sys.stdin.read
    data = input().split()
    
    Q = int(data[0])
    queries = []
    
    index = 1
    for _ in range(Q):
        A = int(data[index])
        B = int(data[index + 1])
        queries.append((A, B))
        index += 2
    
    max_query_value = max(B for _, B in queries)
    appearances = calculate_appearances(max_query_value)
    
    results = query_appearances(queries, appearances)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()