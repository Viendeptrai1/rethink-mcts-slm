def rev(n):
    return int(str(n)[::-1])

def count_appearances(A, B):
    max_val = B
    table = {}
    
    def calculate(i, j):
        if (i, j) in table:
            return table[(i, j)]
        if j == 1:
            result = i
        else:
            result = calculate(i, j - 1) + rev(calculate(i, j - 1))
        table[(i, j)] = result
        return result
    
    count = 0
    for i in range(1, max_val + 1):
        for j in range(1, max_val + 1):
            val = calculate(i, j)
            if A <= val <= B:
                count += 1
    return count

import sys
input = sys.stdin.read
data = input().split()

Q = int(data[0])
queries = [(int(data[i * 2 + 1]), int(data[i * 2 + 2])) for i in range(Q)]

results = [count_appearances(A, B) for A, B in queries]

for result in results:
    print(result)